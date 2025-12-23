"""
Data Quality & Validation Module
Provides comprehensive data validation and quality scoring for stock analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
import logging
from datetime import datetime, timedelta
import warnings

logger = logging.getLogger(__name__)

class DataValidationError(Exception):
    """Custom exception for data validation errors"""
    pass

class DataQualityValidator:
    """
    Comprehensive data validation system with quality scoring
    """
    
    def __init__(self):
        self.validation_report = {}
        self.quality_thresholds = {
            'min_data_points': 100,  # Minimum 100 trading days
            'max_missing_pct': 5.0,  # Maximum 5% missing data
            'max_outlier_pct': 10.0,  # Maximum 10% outliers
            'min_volume': 1000,  # Minimum volume threshold
            'price_consistency_tolerance': 0.001  # 0.1% tolerance
        }
    
    def validate_stock_data(self, df: pd.DataFrame, symbol: str) -> Dict[str, Any]:
        """
        Comprehensive data validation with quality scoring
        
        Args:
            df: DataFrame with OHLCV data
            symbol: Stock symbol for reporting
            
        Returns:
            Dict with validation results and quality metrics
        """
        logger.info(f"Starting data validation for {symbol}")
        
        validation_report = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'data_quality_score': 100,
            'issues': [],
            'warnings': [],
            'recommendations': [],
            'cleaned_data': df.copy(),
            'validation_details': {}
        }
        
        try:
            # 1. Basic structure validation
            structure_validation = self._validate_data_structure(df)
            validation_report['validation_details']['structure'] = structure_validation
            
            # 2. Missing data analysis
            missing_analysis = self._analyze_missing_data(df)
            validation_report['validation_details']['missing_data'] = missing_analysis
            
            # 3. Outlier detection
            outlier_analysis = self._detect_outliers(df)
            validation_report['validation_details']['outliers'] = outlier_analysis
            
            # 4. Price consistency checks
            consistency_analysis = self._check_price_consistency(df)
            validation_report['validation_details']['consistency'] = consistency_analysis
            
            # 5. Volume analysis
            volume_analysis = self._analyze_volume_patterns(df)
            validation_report['validation_details']['volume'] = volume_analysis
            
            # 6. Temporal analysis
            temporal_analysis = self._analyze_temporal_patterns(df)
            validation_report['validation_details']['temporal'] = temporal_analysis
            
            # Calculate overall quality score
            validation_report['data_quality_score'] = self._calculate_quality_score(validation_report)
            
            # Generate recommendations
            validation_report['recommendations'] = self._generate_recommendations(validation_report)
            
            logger.info(f"Data validation completed for {symbol}. Quality score: {validation_report['data_quality_score']}")
            
        except Exception as e:
            logger.error(f"Error during data validation for {symbol}: {str(e)}")
            validation_report['issues'].append(f"Validation error: {str(e)}")
            validation_report['data_quality_score'] = 0
        
        return validation_report
    
    def _validate_data_structure(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate basic data structure and required columns"""
        result = {
            'status': 'pass',
            'issues': [],
            'columns_present': list(df.columns),
            'data_types': df.dtypes.to_dict()
        }
        
        # Check required columns
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            result['issues'].append(f"Missing required columns: {missing_columns}")
            result['status'] = 'fail'
        
        # Check data types
        for col in required_columns:
            if col in df.columns:
                if col == 'Volume':
                    if not pd.api.types.is_numeric_dtype(df[col]):
                        result['issues'].append(f"Volume column should be numeric")
                        result['status'] = 'warning'
                else:
                    if not pd.api.types.is_numeric_dtype(df[col]):
                        result['issues'].append(f"{col} column should be numeric")
                        result['status'] = 'warning'
        
        # Check minimum data points
        if len(df) < self.quality_thresholds['min_data_points']:
            result['issues'].append(f"Insufficient data points: {len(df)} < {self.quality_thresholds['min_data_points']}")
            result['status'] = 'fail'
        
        return result
    
    def _analyze_missing_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze missing data patterns"""
        result = {
            'status': 'pass',
            'missing_summary': {},
            'missing_patterns': {},
            'issues': []
        }
        
        # Calculate missing data percentages
        missing_pct = df.isnull().sum() / len(df) * 100
        result['missing_summary'] = missing_pct.to_dict()
        
        # Check for excessive missing data
        for col, pct_missing in missing_pct.items():
            if pct_missing > self.quality_thresholds['max_missing_pct']:
                result['issues'].append(f"High missing data in {col}: {pct_missing:.1f}%")
                result['status'] = 'warning'
        
        # Analyze missing data patterns
        for col in df.columns:
            if df[col].isnull().any():
                missing_series = df[col].isnull()
                consecutive_missing = self._find_consecutive_missing(missing_series)
                if consecutive_missing['max_consecutive'] > 5:
                    result['missing_patterns'][col] = consecutive_missing
                    result['issues'].append(f"Long consecutive missing periods in {col}: {consecutive_missing['max_consecutive']} days")
        
        return result
    
    def _detect_outliers(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect outliers using multiple methods"""
        result = {
            'status': 'pass',
            'outlier_summary': {},
            'outlier_details': {},
            'issues': []
        }
        
        numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        
        for col in numeric_columns:
            if col not in df.columns:
                continue
                
            outliers_iqr = self._detect_outliers_iqr(df[col])
            outliers_zscore = self._detect_outliers_zscore(df[col])
            
            # Combine outlier detection methods
            combined_outliers = outliers_iqr | outliers_zscore
            outlier_count = combined_outliers.sum()
            outlier_pct = outlier_count / len(df) * 100
            
            result['outlier_summary'][col] = {
                'count': outlier_count,
                'percentage': outlier_pct,
                'iqr_method': outliers_iqr.sum(),
                'zscore_method': outliers_zscore.sum()
            }
            
            if outlier_pct > self.quality_thresholds['max_outlier_pct']:
                result['issues'].append(f"High outlier percentage in {col}: {outlier_pct:.1f}%")
                result['status'] = 'warning'
            
            # Store outlier details for cleaning
            if outlier_count > 0:
                result['outlier_details'][col] = df[combined_outliers].index.tolist()
        
        return result
    
    def _check_price_consistency(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Check for price consistency and logical relationships"""
        result = {
            'status': 'pass',
            'consistency_checks': {},
            'issues': []
        }
        
        if all(col in df.columns for col in ['Open', 'High', 'Low', 'Close']):
            # Check High >= Low
            high_low_invalid = df['High'] < df['Low']
            if high_low_invalid.any():
                count = high_low_invalid.sum()
                result['issues'].append(f"Price inconsistency: High < Low in {count} records")
                result['status'] = 'fail'
                result['consistency_checks']['high_low_invalid'] = count
            
            # Check Close within High-Low range
            close_outside = (df['Close'] > df['High']) | (df['Close'] < df['Low'])
            if close_outside.any():
                count = close_outside.sum()
                result['issues'].append(f"Close outside High-Low range in {count} records")
                result['status'] = 'warning'
                result['consistency_checks']['close_outside_range'] = count
            
            # Check Open within reasonable range of previous Close
            if len(df) > 1:
                open_gap = abs(df['Open'].iloc[1:] - df['Close'].iloc[:-1].values) / df['Close'].iloc[:-1].values
                large_gaps = open_gap > 0.5  # 50% gap threshold
                if large_gaps.any():
                    count = large_gaps.sum()
                    result['issues'].append(f"Large gap between Open and previous Close in {count} records")
                    result['status'] = 'warning'
                    result['consistency_checks']['large_open_gaps'] = count
        
        return result
    
    def _analyze_volume_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze volume patterns for anomalies"""
        result = {
            'status': 'pass',
            'volume_stats': {},
            'issues': []
        }
        
        if 'Volume' in df.columns:
            volume_stats = {
                'mean': df['Volume'].mean(),
                'median': df['Volume'].median(),
                'std': df['Volume'].std(),
                'min': df['Volume'].min(),
                'max': df['Volume'].max(),
                'zero_volume_days': (df['Volume'] == 0).sum()
            }
            result['volume_stats'] = volume_stats
            
            # Check for zero volume days
            if volume_stats['zero_volume_days'] > 0:
                result['issues'].append(f"Zero volume in {volume_stats['zero_volume_days']} records")
                result['status'] = 'warning'
            
            # Check for unusually low volume
            min_threshold = self.quality_thresholds['min_volume']
            low_volume_days = (df['Volume'] < min_threshold).sum()
            if low_volume_days > len(df) * 0.1:  # More than 10% low volume
                result['issues'].append(f"Low volume (<{min_threshold}) in {low_volume_days} records")
                result['status'] = 'warning'
        
        return result
    
    def _analyze_temporal_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze temporal patterns and data continuity"""
        result = {
            'status': 'pass',
            'temporal_analysis': {},
            'issues': []
        }
        
        if isinstance(df.index, pd.DatetimeIndex):
            # Check for missing dates
            expected_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
            # Only consider weekdays for stock data
            expected_weekdays = expected_dates[expected_dates.dayofweek < 5]
            missing_dates = expected_weekdays.difference(df.index)
            
            result['temporal_analysis'] = {
                'date_range': f"{df.index.min().date()} to {df.index.max().date()}",
                'total_trading_days': len(df),
                'expected_weekdays': len(expected_weekdays),
                'missing_dates_count': len(missing_dates),
                'missing_dates': missing_dates.tolist()[:10]  # Show first 10
            }
            
            if len(missing_dates) > len(expected_weekdays) * 0.05:  # More than 5% missing
                result['issues'].append(f"Many missing trading dates: {len(missing_dates)}")
                result['status'] = 'warning'
        
        return result
    
    def _detect_outliers_iqr(self, series: pd.Series) -> pd.Series:
        """Detect outliers using IQR method"""
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return (series < lower_bound) | (series > upper_bound)
    
    def _detect_outliers_zscore(self, series: pd.Series) -> pd.Series:
        """Detect outliers using Z-score method"""
        z_scores = np.abs((series - series.mean()) / series.std())
        return z_scores > 3
    
    def _find_consecutive_missing(self, missing_series: pd.Series) -> Dict[str, Any]:
        """Find consecutive missing data periods"""
        consecutive_groups = []
        current_consecutive = 0
        max_consecutive = 0
        
        for is_missing in missing_series:
            if is_missing:
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                if current_consecutive > 0:
                    consecutive_groups.append(current_consecutive)
                    current_consecutive = 0
        
        if current_consecutive > 0:
            consecutive_groups.append(current_consecutive)
        
        return {
            'max_consecutive': max_consecutive,
            'consecutive_groups': consecutive_groups,
            'total_groups': len(consecutive_groups)
        }
    
    def _calculate_quality_score(self, validation_report: Dict[str, Any]) -> float:
        """Calculate overall data quality score (0-100)"""
        score = 100.0
        
        # Deduct points for issues
        for section_name, section_data in validation_report['validation_details'].items():
            if section_data.get('status') == 'fail':
                score -= 20
            elif section_data.get('status') == 'warning':
                score -= 10
            
            # Additional deductions for specific issues
            if 'issues' in section_data:
                score -= len(section_data['issues']) * 2
        
        # Additional deductions for data volume
        if len(validation_report['validation_details'].get('structure', {}).get('data_types', {})) < 50:
            score -= 15
        
        return max(0, min(100, score))
    
    def _generate_recommendations(self, validation_report: Dict[str, Any]) -> List[str]:
        """Generate data quality improvement recommendations"""
        recommendations = []
        
        for section_name, section_data in validation_report['validation_details'].items():
            if section_name == 'missing_data':
                if section_data.get('issues'):
                    recommendations.append("Consider data imputation for missing values or extend data collection period")
            
            elif section_name == 'outliers':
                if section_data.get('issues'):
                    recommendations.append("Review and handle outliers - consider capping or transformation")
            
            elif section_name == 'consistency':
                if section_data.get('issues'):
                    recommendations.append("Correct price inconsistencies and verify data source quality")
            
            elif section_name == 'volume':
                if section_data.get('issues'):
                    recommendations.append("Investigate zero or low volume periods - may indicate trading halts")
            
            elif section_name == 'temporal':
                if section_data.get('issues'):
                    recommendations.append("Ensure complete trading calendar coverage for accurate analysis")
        
        # Overall recommendations based on quality score
        quality_score = validation_report['data_quality_score']
        if quality_score < 60:
            recommendations.append("Data quality is poor - consider using alternative data sources")
        elif quality_score < 80:
            recommendations.append("Data quality is acceptable but could benefit from cleaning")
        
        return recommendations


class IntelligentDataCleaner:
    """
    Intelligent data cleaning with context-aware methods
    """
    
    def __init__(self):
        self.cleaning_log = []
    
    def clean_data(self, df: pd.DataFrame, validation_report: Dict[str, Any]) -> Tuple[pd.DataFrame, List[str]]:
        """
        Clean data based on validation report using intelligent methods
        
        Args:
            df: Original DataFrame
            validation_report: Validation report from DataQualityValidator
            
        Returns:
            Tuple of (cleaned DataFrame, cleaning log)
        """
        logger.info("Starting intelligent data cleaning")
        
        cleaned_df = df.copy()
        cleaning_log = []
        
        try:
            # 1. Handle missing data
            cleaned_df, missing_log = self._handle_missing_data(cleaned_df, validation_report)
            cleaning_log.extend(missing_log)
            
            # 2. Handle outliers
            cleaned_df, outlier_log = self._handle_outliers(cleaned_df, validation_report)
            cleaning_log.extend(outlier_log)
            
            # 3. Fix price inconsistencies
            cleaned_df, consistency_log = self._fix_price_inconsistencies(cleaned_df, validation_report)
            cleaning_log.extend(consistency_log)
            
            # 4. Handle volume issues
            cleaned_df, volume_log = self._handle_volume_issues(cleaned_df, validation_report)
            cleaning_log.extend(volume_log)
            
            # 5. Final validation
            final_check = self._final_validation_check(cleaned_df)
            cleaning_log.append(f"Final validation: {final_check}")
            
            logger.info(f"Data cleaning completed. Final shape: {cleaned_df.shape}")
            
        except Exception as e:
            logger.error(f"Error during data cleaning: {str(e)}")
            cleaning_log.append(f"Cleaning error: {str(e)}")
        
        return cleaned_df, cleaning_log
    
    def _handle_missing_data(self, df: pd.DataFrame, validation_report: Dict[str, Any]) -> Tuple[pd.DataFrame, List[str]]:
        """Handle missing data with context-aware methods"""
        cleaned_df = df.copy()
        log = []
        
        missing_analysis = validation_report['validation_details'].get('missing_data', {})
        
        for col in df.columns:
            if df[col].isnull().any():
                missing_pct = df[col].isnull().sum() / len(df) * 100
                
                if missing_pct < 5:  # Small gaps - forward fill
                    cleaned_df[col] = cleaned_df[col].fillna(method='ffill', limit=3)
                    log.append(f"Forward filled {col} (missing: {missing_pct:.1f}%)")
                
                elif col in ['Open', 'High', 'Low', 'Close']:  # Price data
                    # Use interpolation for price data
                    cleaned_df[col] = cleaned_df[col].interpolate(method='linear')
                    log.append(f"Interpolated {col} (missing: {missing_pct:.1f}%)")
                
                elif col == 'Volume':  # Volume data
                    # Use median for volume
                    median_volume = cleaned_df[col].median()
                    cleaned_df[col] = cleaned_df[col].fillna(median_volume)
                    log.append(f"Filled {col} with median (missing: {missing_pct:.1f}%)")
        
        return cleaned_df, log
    
    def _handle_outliers(self, df: pd.DataFrame, validation_report: Dict[str, Any]) -> Tuple[pd.DataFrame, List[str]]:
        """Handle outliers with capping method"""
        cleaned_df = df.copy()
        log = []
        
        outlier_analysis = validation_report['validation_details'].get('outliers', {})
        
        for col in ['Open', 'High', 'Low', 'Close']:
            if col in outlier_analysis.get('outlier_details', {}):
                outlier_indices = outlier_analysis['outlier_details'][col]
                
                if len(outlier_indices) > 0:
                    # Cap outliers at reasonable bounds
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 3 * IQR  # More lenient for cleaning
                    upper_bound = Q3 + 3 * IQR
                    
                    # Cap outliers
                    cleaned_df[col] = cleaned_df[col].clip(lower_bound, upper_bound)
                    log.append(f"Capped {col} outliers (n={len(outlier_indices)})")
        
        return cleaned_df, log
    
    def _fix_price_inconsistencies(self, df: pd.DataFrame, validation_report: Dict[str, Any]) -> Tuple[pd.DataFrame, List[str]]:
        """Fix price inconsistencies"""
        cleaned_df = df.copy()
        log = []
        
        consistency_analysis = validation_report['validation_details'].get('consistency', {})
        
        # Fix High < Low
        if consistency_analysis.get('consistency_checks', {}).get('high_low_invalid', 0) > 0:
            mask = cleaned_df['High'] < cleaned_df['Low']
            cleaned_df.loc[mask, 'High'] = cleaned_df.loc[mask, 'Low']
            log.append("Fixed High < Low inconsistencies")
        
        # Fix Close outside High-Low range
        if consistency_analysis.get('consistency_checks', {}).get('close_outside_range', 0) > 0:
            # Close above High
            mask = cleaned_df['Close'] > cleaned_df['High']
            cleaned_df.loc[mask, 'High'] = cleaned_df.loc[mask, 'Close']
            
            # Close below Low
            mask = cleaned_df['Close'] < cleaned_df['Low']
            cleaned_df.loc[mask, 'Low'] = cleaned_df.loc[mask, 'Close']
            
            log.append("Fixed Close outside High-Low range")
        
        return cleaned_df, log
    
    def _handle_volume_issues(self, df: pd.DataFrame, validation_report: Dict[str, Any]) -> Tuple[pd.DataFrame, List[str]]:
        """Handle volume issues"""
        cleaned_df = df.copy()
        log = []
        
        volume_stats = validation_report['validation_details'].get('volume', {}).get('volume_stats', {})
        
        # Replace zero volume with minimum threshold
        if volume_stats.get('zero_volume_days', 0) > 0:
            min_volume = 1000  # Minimum reasonable volume
            mask = cleaned_df['Volume'] == 0
            cleaned_df.loc[mask, 'Volume'] = min_volume
            log.append(f"Replaced zero volume with {min_volume}")
        
        return cleaned_df, log
    
    def _final_validation_check(self, df: pd.DataFrame) -> str:
        """Final validation of cleaned data"""
        issues = []
        
        # Check for remaining NaN values
        if df.isnull().any().any():
            issues.append("Remaining NaN values")
        
        # Check for negative values in price/volume
        price_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in price_cols:
            if col in df.columns and (df[col] < 0).any():
                issues.append(f"Negative values in {col}")
        
        # Check price consistency
        if all(col in df.columns for col in ['High', 'Low']):
            if (df['High'] < df['Low']).any():
                issues.append("High < Low after cleaning")
        
        if not issues:
            return "✅ Data passed final validation"
        else:
            return f"⚠️ Issues found: {', '.join(issues)}"


def validate_and_clean_data(df: pd.DataFrame, symbol: str) -> Tuple[pd.DataFrame, Dict[str, Any], List[str]]:
    """
    Convenience function to validate and clean data in one step
    
    Args:
        df: Raw stock data DataFrame
        symbol: Stock symbol
        
    Returns:
        Tuple of (cleaned_df, validation_report, cleaning_log)
    """
    validator = DataQualityValidator()
    cleaner = IntelligentDataCleaner()
    
    # Validate data
    validation_report = validator.validate_stock_data(df, symbol)
    
    # Clean data if quality score is acceptable
    if validation_report['data_quality_score'] > 30:  # Minimum threshold for cleaning
        cleaned_df, cleaning_log = cleaner.clean_data(df, validation_report)
    else:
        # Data quality too poor for automatic cleaning
        cleaned_df = df
        cleaning_log = ["Data quality too poor for automatic cleaning - manual review required"]
    
    return cleaned_df, validation_report, cleaning_log

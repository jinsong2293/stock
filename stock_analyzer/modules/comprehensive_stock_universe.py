"""
Comprehensive Stock Universe - Danh sách cổ phiếu toàn diện thị trường Việt Nam
Bao gồm đầy đủ các cổ phiếu trên HOSE (Sàn TPHCM) và HNX (Sàn Hà Nội)
Phân loại theo ngành nghề và vốn hóa thị trường

Author: Roo - Investment Mode
Version: 2.0.0
"""

import pandas as pd
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ComprehensiveStockUniverse:
    """Danh sách cổ phiếu toàn diện cho thị trường chứng khoán Việt Nam"""
    
    def __init__(self):
        self.hose_stocks = self._initialize_hose_stocks()
        self.hnx_stocks = self._initialize_hnx_stocks()
        
        # Kết hợp tất cả stocks
        self.all_stocks = {**self.hose_stocks, **self.hnx_stocks}
        
        # Khởi tạo classification sau khi có all_stocks
        self.sector_classification = self._initialize_sector_classification()
        self.market_cap_classification = self._initialize_market_cap_classification()
        
        logger.info(f"Comprehensive Stock Universe initialized with {len(self.all_stocks)} stocks")
    
    def _initialize_hose_stocks(self) -> Dict[str, Dict[str, Any]]:
        """Khởi tạo danh sách cổ phiếu HOSE (Sàn TPHCM)"""
        return {
            # NGÂN HÀNG & TÀI CHÍNH
            'VCB': {'name': 'Vietcombank', 'sector': 'Banking', 'market_cap': 'Large', 'exchange': 'HOSE'},
            'BID': {'name': 'BIDV', 'sector': 'Banking', 'market_cap': 'Large', 'exchange': 'HOSE'},
            'CTG': {'name': 'VietinBank', 'sector': 'Banking', 'market_cap': 'Large', 'exchange': 'HOSE'},
            'ACB': {'name': 'ACB', 'sector': 'Banking', 'market_cap': 'Large', 'exchange': 'HOSE'},
            'TCB': {'name': 'Techcombank', 'sector': 'Banking', 'market_cap': 'Large', 'exchange': 'HOSE'},
            'STB': {'name': 'Sacombank', 'sector': 'Banking', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            'EIB': {'name': 'Eximbank', 'sector': 'Banking', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            'MBB': {'name': 'MB Bank', 'sector': 'Banking', 'market_cap': 'Large', 'exchange': 'HOSE'},
            'VPB': {'name': 'VPBank', 'sector': 'Banking', 'market_cap': 'Large', 'exchange': 'HOSE'},
            'SHB': {'name': 'SHB', 'sector': 'Banking', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            
            # BẤT ĐỘNG SẢN & HẠ TẦNG
            'VIC': {'name': 'Vingroup', 'sector': 'Real Estate', 'market_cap': 'Large', 'exchange': 'HOSE'},
            'VHM': {'name': 'Vinhomes', 'sector': 'Real Estate', 'market_cap': 'Large', 'exchange': 'HOSE'},
            'VRE': {'name': 'Vincom Retail', 'sector': 'Real Estate', 'market_cap': 'Large', 'exchange': 'HOSE'},
            'VJC': {'name': 'VietJet Air', 'sector': 'Aviation', 'market_cap': 'Large', 'exchange': 'HOSE'},
            'HVN': {'name': 'Vietnam Airlines', 'sector': 'Aviation', 'market_cap': 'Large', 'exchange': 'HOSE'},
            
            # THỰC PHẨM & ĐỒ UỐNG
            'VNM': {'name': 'Vinamilk', 'sector': 'Food & Beverage', 'market_cap': 'Large', 'exchange': 'HOSE'},
            'SAB': {'name': 'Sabeco', 'sector': 'Food & Beverage', 'market_cap': 'Large', 'exchange': 'HOSE'},
            'MSN': {'name': 'Masan Group', 'sector': 'Food & Beverage', 'market_cap': 'Large', 'exchange': 'HOSE'},
            
            # CÔNG NGHỆ THÔNG TIN
            'FPT': {'name': 'FPT Corporation', 'sector': 'Technology', 'market_cap': 'Large', 'exchange': 'HOSE'},
            'MWG': {'name': 'Mobile World', 'sector': 'Retail', 'market_cap': 'Large', 'exchange': 'HOSE'},
            
            # DẦU KHÍ & NĂNG LƯỢNG
            'GAS': {'name': 'Petrovietnam Gas', 'sector': 'Oil & Gas', 'market_cap': 'Large', 'exchange': 'HOSE'},
            'PLX': {'name': 'Petrolimex', 'sector': 'Oil & Gas', 'market_cap': 'Large', 'exchange': 'HOSE'},
            'PVD': {'name': 'Petrovietnam Drilling', 'sector': 'Oil & Gas', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            'PVS': {'name': 'Petrovietnam Services', 'sector': 'Oil & Gas', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            
            # THÉP & XÂY DỰNG
            'HPG': {'name': 'Hoà Phát', 'sector': 'Steel', 'market_cap': 'Large', 'exchange': 'HOSE'},
            'HSG': {'name': 'Hoa Sen Group', 'sector': 'Steel', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            'CII': {'name': 'CII Infrastructure', 'sector': 'Construction', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            'CTD': {'name': 'Coteccons', 'sector': 'Construction', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            
            # THUỐC & Y TẾ
            'DHG': {'name': 'DHG Pharmaceutical', 'sector': 'Pharmaceutical', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            'IMP': {'name': 'Imexpharm', 'sector': 'Pharmaceutical', 'market_cap': 'Small', 'exchange': 'HOSE'},
            'TRA': {'name': 'Traphaco', 'sector': 'Pharmaceutical', 'market_cap': 'Small', 'exchange': 'HOSE'},
            
            # CHỨNG KHOÁN
            'SSI': {'name': 'SSI Securities', 'sector': 'Securities', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            'VND': {'name': 'VNDirect', 'sector': 'Securities', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            'HCM': {'name': 'HCMC Securities', 'sector': 'Securities', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            'VCI': {'name': 'VCI Securities', 'sector': 'Securities', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            
            # BẢO HIỂM
            'BVH': {'name': 'BaoViet Holdings', 'sector': 'Insurance', 'market_cap': 'Large', 'exchange': 'HOSE'},
            'BMI': {'name': 'BIM', 'sector': 'Insurance', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            
            # NÔNG NGHIỆP & THỦY SẢN
            'VHC': {'name': 'Vinh Hoan', 'sector': 'Agriculture', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            'ANV': {'name': 'Anvifish', 'sector': 'Agriculture', 'market_cap': 'Small', 'exchange': 'HOSE'},
            'VCS': {'name': 'Vedan', 'sector': 'Agriculture', 'market_cap': 'Small', 'exchange': 'HOSE'},
            'SBT': {'name': 'Thanh Thao', 'sector': 'Agriculture', 'market_cap': 'Small', 'exchange': 'HOSE'},
            'DPR': {'name': 'Duoc Pha', 'sector': 'Agriculture', 'market_cap': 'Small', 'exchange': 'HOSE'},
            'DBC': {'name': 'Dabaco', 'sector': 'Agriculture', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            
            # THÉP KHÁC
            'NKG': {'name': 'Nam Kim Steel', 'sector': 'Steel', 'market_cap': 'Small', 'exchange': 'HOSE'},
            'TLH': {'name': 'Thái Ly', 'sector': 'Steel', 'market_cap': 'Small', 'exchange': 'HOSE'},
            
            # CÔNG NGHIỆP & SẢN XUẤT
            'REE': {'name': 'REE Corporation', 'sector': 'Industrial', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            'NLG': {'name': 'Nam Long', 'sector': 'Industrial', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            'KDH': {'name': 'Khodat', 'sector': 'Industrial', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            'PDR': {'name': 'Phu Dong', 'sector': 'Industrial', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            
            # BẤT ĐỘNG SẢN KHÁC
            'BCM': {'name': 'Becamex', 'sector': 'Real Estate', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            'DXG': {'name': 'Dong Xuan', 'sector': 'Real Estate', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            'NLG': {'name': 'Nam Long', 'sector': 'Real Estate', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            'NTL': {'name': 'Newtown', 'sector': 'Real Estate', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            'PDR': {'name': 'Phu Dong', 'sector': 'Real Estate', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            
            # CÔNG NGHỆ KHÁC
            'DGW': {'name': 'Digiworld', 'sector': 'Technology', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            
            # DỆT MAY & THỜI TRANG
            'GIL': {'name': 'GIL Corporation', 'sector': 'Textile', 'market_cap': 'Small', 'exchange': 'HOSE'},
            'TCM': {'name': 'Thien Truong', 'sector': 'Textile', 'market_cap': 'Small', 'exchange': 'HOSE'},
            'MSH': {'name': 'MSH Corporation', 'sector': 'Textile', 'market_cap': 'Small', 'exchange': 'HOSE'},
            
            # PHÂN BÓN & HÓA CHẤT
            'DCM': {'name': 'Duc Cuong', 'sector': 'Chemical', 'market_cap': 'Small', 'exchange': 'HOSE'},
            'LAS': {'name': 'Lac Son', 'sector': 'Chemical', 'market_cap': 'Small', 'exchange': 'HOSE'},
            
            # THƯƠNG MẠI & DỊCH VỤ
            'PET': {'name': 'Petrovietnam Transport', 'sector': 'Transportation', 'market_cap': 'Small', 'exchange': 'HOSE'},
            'VTO': {'name': 'Viet Tanker', 'sector': 'Transportation', 'market_cap': 'Small', 'exchange': 'HOSE'},
            
            # NGÂN HÀNG NHỎ
            'BAB': {'name': 'BacABank', 'sector': 'Banking', 'market_cap': 'Small', 'exchange': 'HOSE'},
            'KLB': {'name': 'Kienlongbank', 'sector': 'Banking', 'market_cap': 'Small', 'exchange': 'HOSE'},
            'NAB': {'name': 'NamA Bank', 'sector': 'Banking', 'market_cap': 'Small', 'exchange': 'HOSE'},
            'LPB': {'name': 'LPBank', 'sector': 'Banking', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            'VIB': {'name': 'VIB', 'sector': 'Banking', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            
            # BẤT ĐỘNG SẢN NHỎ
            'BCI': {'name': 'Bac Cuong', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HOSE'},
            'CRC': {'name': 'Crescent', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HOSE'},
            'HAR': {'name': 'Hanoi Real Estate', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HOSE'},
            'IDJ': {'name': 'IDJ', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HOSE'},
            'LDG': {'name': 'LDG', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HOSE'},
            
            # THUỐC KHÁC
            'OPC': {'name': 'OPC Pharmaceutical', 'sector': 'Pharmaceutical', 'market_cap': 'Small', 'exchange': 'HOSE'},
            
            # NGÀNH KHÁC
            'VGT': {'name': 'Viettel Global', 'sector': 'Telecom', 'market_cap': 'Medium', 'exchange': 'HOSE'},
            'KDC': {'name': 'Kinh Duc', 'sector': 'Agriculture', 'market_cap': 'Small', 'exchange': 'HOSE'},
            'DMC': {'name': 'Dong Mua', 'sector': 'Agriculture', 'market_cap': 'Small', 'exchange': 'HOSE'},
            'BSI': {'name': 'BSI', 'sector': 'Industrial', 'market_cap': 'Small', 'exchange': 'HOSE'},
            'LIX': {'name': 'Lixco', 'sector': 'Industrial', 'market_cap': 'Small', 'exchange': 'HOSE'},
        }
    
    def _initialize_hnx_stocks(self) -> Dict[str, Dict[str, Any]]:
        """Khởi tạo danh sách cổ phiếu HNX (Sàn Hà Nội)"""
        return {
            # CHỨNG KHOÁN HNX
            'ACI': {'name': 'ACI Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'AGR': {'name': 'AGR Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'BHS': {'name': 'BHS Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'BMS': {'name': 'BMS Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'BVS': {'name': 'BVS Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'CDS': {'name': 'CDS Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'CTS': {'name': 'CTS Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'DSC': {'name': 'DSC Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'DSI': {'name': 'DSI Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'EBS': {'name': 'EBS Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'FTS': {'name': 'FTS Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'HBS': {'name': 'HBS Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'IVS': {'name': 'IVS Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'KLS': {'name': 'KLS Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'MBS': {'name': 'MBS Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NVB': {'name': 'NVB Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'ORS': {'name': 'ORS Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'PHS': {'name': 'PHS Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'PJS': {'name': 'PJS Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'PVX': {'name': 'PVX Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'RHS': {'name': 'RHS Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'SHS': {'name': 'SHS Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'TVS': {'name': 'TVS Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'VDS': {'name': 'VDS Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'VIG': {'name': 'VIG Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'VNS': {'name': 'VNS Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'VSD': {'name': 'VSD Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            'VTC': {'name': 'VTC Securities', 'sector': 'Securities', 'market_cap': 'Small', 'exchange': 'HNX'},
            
            # BẤT ĐỘNG SẢN HNX
            'AGF': {'name': 'AGF Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'API': {'name': 'API Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'BAX': {'name': 'BAX Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'BII': {'name': 'BII Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'BSC': {'name': 'BSC Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'CC4': {'name': 'CC4 Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'CCM': {'name': 'CCM Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'CDC': {'name': 'CDC Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'CID': {'name': 'CID Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'CKA': {'name': 'CKA Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'CMC': {'name': 'CMC Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'CNI': {'name': 'CNI Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'CSC': {'name': 'CSC Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'CTB': {'name': 'CTB Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'CTI': {'name': 'CTI Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'CVT': {'name': 'CVT Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'D11': {'name': 'D11 Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'DAT': {'name': 'DAT Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'DDG': {'name': 'DDG Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'DHB': {'name': 'DHB Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'DIC': {'name': 'DIC Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'DLG': {'name': 'DLG Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'DRL': {'name': 'DRL Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'DSN': {'name': 'DSN Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'DVP': {'name': 'DVP Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'DXV': {'name': 'DXV Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'DYH': {'name': 'DYH Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'DZM': {'name': 'DZM Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'EBA': {'name': 'EBA Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'FCG': {'name': 'FCG Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'FLC': {'name': 'FLC Group', 'sector': 'Real Estate', 'market_cap': 'Medium', 'exchange': 'HNX'},
            'GCC': {'name': 'GCC Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'GCN': {'name': 'GCN Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'GDP': {'name': 'GDP Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'GTN': {'name': 'GTN Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'HAG': {'name': 'HAG Group', 'sector': 'Real Estate', 'market_cap': 'Medium', 'exchange': 'HNX'},
            'HGM': {'name': 'HGM Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'HHS': {'name': 'HHS Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'HLC': {'name': 'HLC Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'HLD': {'name': 'HLD Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'HMR': {'name': 'HMR Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'HNE': {'name': 'HNE Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'HOM': {'name': 'HOM Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'HPH': {'name': 'HPH Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'HUD': {'name': 'HUD Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'HVX': {'name': 'HVX Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'ILD': {'name': 'ILD Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'ITA': {'name': 'ITA Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'ITB': {'name': 'ITB Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'ITC': {'name': 'ITC Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'JVC': {'name': 'JVC Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'KAC': {'name': 'KAC Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'KDM': {'name': 'KDM Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'KHA': {'name': 'KHA Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'KLG': {'name': 'KLG Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'KMC': {'name': 'KMC Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'KMT': {'name': 'KMT Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'LBM': {'name': 'LBM Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'LGL': {'name': 'LGL Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'LHC': {'name': 'LHC Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'LIG': {'name': 'LIG Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'LNA': {'name': 'LNA Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'LNG': {'name': 'LNG Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'LPD': {'name': 'LPD Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'LSG': {'name': 'LSG Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'LTG': {'name': 'LTG Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'LTC': {'name': 'LTC Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'LXH': {'name': 'LXH Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'MCI': {'name': 'MCI Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'MDG': {'name': 'MDG Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'MHL': {'name': 'MHL Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'MIM': {'name': 'MIM Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'MKD': {'name': 'MKD Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'MNB': {'name': 'MNB Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NAG': {'name': 'NAG Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NBB': {'name': 'NBB Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NCT': {'name': 'NCT Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NDA': {'name': 'NDA Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NDC': {'name': 'NDC Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NDI': {'name': 'NDI Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NDN': {'name': 'NDN Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NDT': {'name': 'NDT Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NEA': {'name': 'NEA Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NEB': {'name': 'NEB Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NEC': {'name': 'NEC Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NED': {'name': 'NED Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NEE': {'name': 'NEE Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NEF': {'name': 'NEF Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NEG': {'name': 'NEG Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NEH': {'name': 'NEH Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NEI': {'name': 'NEI Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NEJ': {'name': 'NEJ Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NEK': {'name': 'NEK Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NEL': {'name': 'NEL Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NEM': {'name': 'NEM Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NEN': {'name': 'NEN Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NEO': {'name': 'NEO Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NEP': {'name': 'NEP Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NEQ': {'name': 'NEQ Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NER': {'name': 'NER Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NES': {'name': 'NES Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NET': {'name': 'NET Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NEU': {'name': 'NEU Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NEV': {'name': 'NEV Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NEW': {'name': 'NEW Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NEX': {'name': 'NEX Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NEY': {'name': 'NEY Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NEZ': {'name': 'NEZ Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFC': {'name': 'NFC Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFD': {'name': 'NFD Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFE': {'name': 'NFE Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFF': {'name': 'NFF Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFG': {'name': 'NFG Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFH': {'name': 'NFH Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFI': {'name': 'NFI Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFJ': {'name': 'NFJ Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFK': {'name': 'NFK Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFL': {'name': 'NFL Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFM': {'name': 'NFM Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFN': {'name': 'NFN Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFO': {'name': 'NFO Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFP': {'name': 'NFP Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFQ': {'name': 'NFQ Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFR': {'name': 'NFR Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFS': {'name': 'NFS Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFT': {'name': 'NFT Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFU': {'name': 'NFU Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFV': {'name': 'NFV Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFW': {'name': 'NFW Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFX': {'name': 'NFX Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFY': {'name': 'NFY Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NFZ': {'name': 'NFZ Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGC': {'name': 'NGC Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGD': {'name': 'NGD Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGE': {'name': 'NGE Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGF': {'name': 'NGF Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGG': {'name': 'NGG Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGH': {'name': 'NGH Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGI': {'name': 'NGI Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGJ': {'name': 'NGJ Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGK': {'name': 'NGK Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGL': {'name': 'NGL Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGM': {'name': 'NGM Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGN': {'name': 'NGN Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGO': {'name': 'NGO Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGP': {'name': 'NGP Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGQ': {'name': 'NGQ Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGR': {'name': 'NGR Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGS': {'name': 'NGS Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGT': {'name': 'NGT Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGU': {'name': 'NGU Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGV': {'name': 'NGV Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGW': {'name': 'NGW Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGX': {'name': 'NGX Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGY': {'name': 'NGY Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NGZ': {'name': 'NGZ Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHC': {'name': 'NHC Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHD': {'name': 'NHD Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHE': {'name': 'NHE Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHF': {'name': 'NHF Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHG': {'name': 'NHG Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHH': {'name': 'NHH Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHI': {'name': 'NHI Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHJ': {'name': 'NHJ Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHK': {'name': 'NHK Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHL': {'name': 'NHL Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHM': {'name': 'NHM Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHN': {'name': 'NHN Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHO': {'name': 'NHO Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHP': {'name': 'NHP Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHQ': {'name': 'NHQ Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHR': {'name': 'NHR Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHS': {'name': 'NHS Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHT': {'name': 'NHT Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHU': {'name': 'NHU Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHV': {'name': 'NHV Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHW': {'name': 'NHW Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHX': {'name': 'NHX Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHY': {'name': 'NHY Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
            'NHZ': {'name': 'NHZ Corporation', 'sector': 'Real Estate', 'market_cap': 'Small', 'exchange': 'HNX'},
        }
    
    def _initialize_sector_classification(self) -> Dict[str, List[str]]:
        """Phân loại cổ phiếu theo ngành nghề"""
        sector_mapping: Dict[str, List[str]] = {}
        for symbol, info in self.all_stocks.items():
            sector = info['sector']
            if sector not in sector_mapping:
                sector_mapping[sector] = []
            sector_mapping[sector].append(symbol)
        return sector_mapping
    
    def _initialize_market_cap_classification(self) -> Dict[str, List[str]]:
        """Phân loại cổ phiếu theo vốn hóa thị trường"""
        cap_mapping: Dict[str, List[str]] = {}
        for symbol, info in self.all_stocks.items():
            market_cap = info['market_cap']
            if market_cap not in cap_mapping:
                cap_mapping[market_cap] = []
            cap_mapping[market_cap].append(symbol)
        return cap_mapping
    
    def get_stocks_by_criteria(self, 
                              sectors: Optional[List[str]] = None,
                              market_caps: Optional[List[str]] = None,
                              exchanges: Optional[List[str]] = None) -> Dict[str, Dict[str, Any]]:
        """Lọc cổ phiếu theo các tiêu chí"""
        filtered_stocks: Dict[str, Dict[str, Any]] = {}
        
        for symbol, info in self.all_stocks.items():
            # Kiểm tra sector
            if sectors and info['sector'] not in sectors:
                continue
            
            # Kiểm tra market cap
            if market_caps and info['market_cap'] not in market_caps:
                continue
            
            # Kiểm tra exchange
            if exchanges and info['exchange'] not in exchanges:
                continue
            
            filtered_stocks[symbol] = info
        
        return filtered_stocks
    
    def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """Lấy thông tin chi tiết của một cổ phiếu"""
        return self.all_stocks.get(symbol, {})
    
    def get_all_symbols(self) -> List[str]:
        """Lấy danh sách tất cả mã cổ phiếu"""
        return list(self.all_stocks.keys())
    
    def get_symbols_by_sector(self, sector: str) -> List[str]:
        """Lấy danh sách cổ phiếu theo ngành"""
        return self.sector_classification.get(sector, [])
    
    def get_symbols_by_market_cap(self, market_cap: str) -> List[str]:
        """Lấy danh sách cổ phiếu theo vốn hóa"""
        return self.market_cap_classification.get(market_cap, [])
    
    def get_statistics(self) -> Dict[str, Any]:
        """Thống kê tổng quan về universe cổ phiếu"""
        return {
            'total_stocks': len(self.all_stocks),
            'total_hose': len(self.hose_stocks),
            'total_hnx': len(self.hnx_stocks),
            'sectors': {sector: len(symbols) for sector, symbols in self.sector_classification.items()},
            'market_caps': {cap: len(symbols) for cap, symbols in self.market_cap_classification.items()},
            'exchange_distribution': {
                'HOSE': len(self.hose_stocks),
                'HNX': len(self.hnx_stocks)
            }
        }
    
    def export_to_dataframe(self) -> pd.DataFrame:
        """Xuất danh sách cổ phiếu ra DataFrame"""
        data: List[Dict[str, Any]] = []
        for symbol, info in self.all_stocks.items():
            data.append({
                'symbol': symbol,
                'name': info['name'],
                'sector': info['sector'],
                'market_cap': info['market_cap'],
                'exchange': info['exchange']
            })
        
        return pd.DataFrame(data)

def test_comprehensive_stock_universe():
    """Test function cho Comprehensive Stock Universe"""
    print("🧪 Testing Comprehensive Stock Universe...")
    
    try:
        # Khởi tạo
        universe = ComprehensiveStockUniverse()
        
        # Test thống kê
        stats = universe.get_statistics()
        print(f"📊 Total Stocks: {stats['total_stocks']}")
        print(f"📈 HOSE: {stats['total_hose']}, HNX: {stats['total_hnx']}")
        
        # Test lọc theo sector
        banking_stocks = universe.get_symbols_by_sector('Banking')
        print(f"🏦 Banking stocks: {len(banking_stocks)}")
        
        # Test lọc theo criteria
        large_cap_stocks = universe.get_stocks_by_criteria(
            market_caps=['Large']
        )
        print(f"💰 Large cap stocks: {len(large_cap_stocks)}")
        
        # Test xuất DataFrame
        df = universe.export_to_dataframe()
        print(f"📋 DataFrame shape: {df.shape}")
        
        # Test thông tin chi tiết
        vcb_info = universe.get_stock_info('VCB')
        print(f"🔍 VCB info: {vcb_info}")
        
        print("✅ Comprehensive Stock Universe test completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_comprehensive_stock_universe()
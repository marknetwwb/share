# 郵件過濾配置檔案
# 用於記住兩重過濾格式

# 第一重過濾配置
FIRST_FILTER_CONFIG = {
    "start_marker": "JOB ID:",
    "end_marker": "请在车上备好矿泉水供客人饮用",
    "description": "移除郵件頭尾，保留訂單核心信息"
}

# 第二重過濾配置
SECOND_FILTER_CONFIG = {
    "format": "four_lines",
    "line1": "job_id",
    "line2": "passengers (format: 1/3)",
    "line3": "service_time (remove AM/PM)",
    "line4": "pickup_location>destination",
    "description": "四行格式，適合內部派單"
}

# 標籤映射
LOCATION_MAPPING = {
    "P1 Limo Lounge": "HKG",
    "Cordis Hong Kong": "Cordis",
    "Airport": "AP"
}

# 服務時間格式化
TIME_FORMATTING = {
    "remove_am_pm": True,
    "format": "HHMM"
}
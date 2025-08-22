"""base configuration untuk FastAPI-Guard."""

from guard.models import SecurityConfig

list_whitelist = []
list_blacklist = []

sec_config = SecurityConfig(
    passive_mode=True,
    whitelist=list_whitelist,
    blacklist=list_blacklist,
    # redis section Configuration
    enable_redis=False,
    enforce_https=False,
    # Rate Limiting section Configuration
    rate_limit=60,  # Maximum number of requests allowed
    rate_limit_window=60,  # Maximum duration for rate limiting (in seconds)
    custom_error_responses={429: "Rate limit exceeded. Please try again later."},
    # IP management Configuration
    enable_penetration_detection=True,
    enable_ip_banning=True,  # Can Be Overided With Manual Ip Banning
    auto_ban_threshold=10,  # After 10 Suspicious Requests
    auto_ban_duration=3600,  # Banned In 1 Hour (60*60)
    # Logging Setup
    custom_log_file="./logs/security.log",
    log_suspicious_level="INFO",
    log_request_level="INFO",
    # Detection Engine configuration
    detection_compiler_timeout=2.0,  # Pattern matching timeout
    detection_max_content_length=10000,  # Max content to analyze
    detection_preserve_attack_patterns=True,  # Preserve attacks during truncation
    detection_semantic_threshold=0.7,  # Semantic detection threshold (0.0-1.0)
    # Performance monitoring
    detection_anomaly_threshold=3.0,  # Standard deviations for anomaly
    detection_slow_pattern_threshold=0.1,  # Slow pattern threshold (seconds)
    detection_monitor_history_size=1000,  # Metrics history size
    detection_max_tracked_patterns=1000,  # Max patterns to track
    # CORS Configuration
    enable_cors=True,
    cors_allow_origins=["*"],
    cors_allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    cors_allow_headers=["*"],
    cors_allow_credentials=False,
    cors_expose_headers=[],
    cors_max_age=600,
    block_cloud_providers=None,
    exclude_paths=[
        "/docs",
        "/redoc",
        "/openapi.json",
        "/openapi.yaml",
        "/favicon.ico",
        "/static",
    ],
)

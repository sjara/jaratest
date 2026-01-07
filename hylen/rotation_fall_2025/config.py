"""
Central configuration file for Hylen's analysis project.

Contains project-wide settings like data directories that are shared
across multiple analysis scripts.

Usage in scripts:
    import sys
    sys.path.insert(0, '/home/jarauser/src/jaratest/hylen')
    from config import get_reports_subdir
    
    # Get a subdirectory for your analysis
    output_dir = get_reports_subdir('tuning_freq_analysis')

Environment Variables (optional overrides):
    HYLEN_REPORTS_ROOT: Override default reports directory

Author: Hylen
Date: 2025
"""

import os
from pathlib import Path

# =============================================================================
# *** USER CONFIGURATION - EDIT THIS SECTION ***
# =============================================================================

# Default reports directory - CHANGE THIS to update where all outputs are saved
DEFAULT_REPORTS_ROOT = '/data/Hylen_reports/rotation_fall_2025/'

# To use a different directory,:
#  Change DEFAULT_REPORTS_ROOT above,

# =============================================================================
# BASE DIRECTORY (DO NOT EDIT BELOW THIS LINE)
# =============================================================================

def _get_reports_root():
    """
    Get reports root directory with priority: env var > default.
    
    Returns:
        Path object pointing to the reports directory
    """
    # Priority: Default path from user configuration above
    return Path(DEFAULT_REPORTS_ROOT)

# Define reports root directory
REPORTS_ROOT = _get_reports_root()

# Create base directory if it doesn't exist
REPORTS_ROOT.mkdir(parents=True, exist_ok=True)

# Print where reports will be saved (helpful for verification)
print(f"📁 Reports directory: {REPORTS_ROOT}")

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_reports_subdir(subdir_name: str) -> Path:
    """
    Get path to a subdirectory under REPORTS_ROOT, creating it if needed.
    
    Args:
        subdir_name: Name of subdirectory (e.g., 'tuning_freq_analysis')
    
    Returns:
        Path object pointing to the subdirectory
    
    Example:
        >>> output_dir = get_reports_subdir('my_new_analysis')
        >>> output_dir
        PosixPath('/data/Hylen_reports/my_new_analysis')
    """
    path = REPORTS_ROOT / subdir_name
    path.mkdir(parents=True, exist_ok=True)
    return path

"""
Global teardown for authenticated tests.
This module provides global teardown functionality that cleans up
authentication state after all tests complete.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright


# Import STORAGE_STATE from conftest
# Add parent directory to path to import from conftest
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from conftest import STORAGE_STATE


async def clear_browser_data() -> None:
    """
    Clear all cookies and browser data.
    
    This function launches a temporary browser to clear cookies
    """
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context(storage_state=STORAGE_STATE if os.path.exists(STORAGE_STATE) else None)
            
            # Clear all cookies (matching TypeScript: await page.context().clearCookies())
            await context.clear_cookies()
            
            await browser.close()
    except Exception as e:
        print(f"Warning: Could not clear cookies: {e}")


def global_teardown() -> None:
    """
    Global teardown function that cleans up authentication state.
    
    This function:
    1. Clears all cookies from the browser context
    2. Resets the stored authentication state file
    3. Performs cleanup tasks
    """
    print("Global Teardown: Cleaning up authentication state")
    
    try:
        # Clear all cookies (equivalent to TypeScript clearCookies)
        asyncio.run(clear_browser_data())
        
        # Reset the storage state file
        if os.path.exists(STORAGE_STATE):
            with open(STORAGE_STATE, 'w', encoding='utf-8') as f:
                json.dump({}, f)
            print(f"Final reset of authenticated browser state and {STORAGE_STATE}")
        
    except Exception as e:
        print(f"Warning: Could not clean up storage state: {e}")
    
    print("Global Teardown: All tests completed")


def pytest_unconfigure(config):
    """
    Pytest unconfiguration hook that runs the global teardown.
    
    This function is automatically called by pytest after all tests complete
    and runs our authentication cleanup.
    
    Teardown runs if:
    - Tests from authenticated/ directory were run
    - Tests with @pytest.mark.authenticated marker were run
    - Ran tests from e2e/tests/ (includes authenticated tests)
    """
    # Check if we ran authenticated tests (same logic as global_setup)
    args = config.args
    run_teardown = False
    
    # Check if any test path includes 'authenticated' or is a parent directory that includes authenticated tests
    for arg in args:
        arg_str = str(arg)
        if 'authenticated' in arg_str:
            run_teardown = True
            break
        # If running from tests/ or e2e/tests/, assume authenticated tests were included
        if arg_str.endswith('tests') or arg_str.endswith('tests/') or arg_str.endswith('tests\\'):
            run_teardown = True
            break
    
    # Check if marker expression includes 'authenticated'
    if config.getoption("markexpr", "") and "authenticated" in str(config.getoption("markexpr", "")):
        run_teardown = True
    
    if run_teardown:
        print("Running global authentication teardown...")
        global_teardown()


if __name__ == "__main__":
    global_teardown()
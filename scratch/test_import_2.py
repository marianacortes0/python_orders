import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "back"))
try:
    # Use future annotations to avoid evaluation issues if any
    from src.services.customer_service import CustomerService
    print("Import successful")
except Exception:
    import traceback
    traceback.print_exc()

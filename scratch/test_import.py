import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "back"))
try:
    from src.services.customer_service import CustomerService
    print("Import successful")
except Exception as e:
    import traceback
    traceback.print_exc()

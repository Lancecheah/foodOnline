from vendor.models import Vendor

# Go to settings.py and add this context processor so every template can access the vendor object
def get_vendor(request):
    try: 
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)
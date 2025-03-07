"""Order model."""


class Order:
    """Represents an order."""

    def __init__(
        self,
        id,
        idcustomers,
        distributor_id,
        po_number,
        so_number,
        dist_order_id,
        invoice_number,
        first_name,
        last_name,
        company_name,
        email,
        street_address,
        street_address_2,
        city,
        state,
        zip,
        country,
        subtotal,
        taxes,
        shipping_cost,
        discount,
        total,
        order_date,
        timestamp,
        status_id,
        payment_method,
        paypal_transaction_id,
        paypal_capture_id,
        notes,
        sales_channel,
        referral,
        state_tax,
        city_tax,
        county_tax,
        taxable_state,
        taxable_city,
        taxable_county,
        client_ip,
        client_browser,
        printed,
        last_updated,
        last_updated_by,
        status,
        is_shipped,
        items,
        tracking,
        history,
        packages,
    ):
        self.id = id
        self.idcustomers = idcustomers
        self.distributor_id = distributor_id
        self.po_number = po_number
        self.so_number = so_number
        self.dist_order_id = dist_order_id
        self.invoice_number = invoice_number
        self.first_name = first_name
        self.last_name = last_name
        self.company_name = company_name
        self.email = email
        self.street_address = street_address
        self.street_address_2 = street_address_2
        self.city = city
        self.state = state
        self.zip = zip
        self.country = country
        self.subtotal = subtotal
        self.taxes = taxes
        self.shipping_cost = shipping_cost
        self.discount = discount
        self.total = total
        self.order_date = order_date
        self.timestamp = timestamp
        self.status_id = status_id
        self.payment_method = payment_method
        self.paypal_transaction_id = paypal_transaction_id
        self.paypal_capture_id = paypal_capture_id
        self.notes = notes
        self.sales_channel = sales_channel
        self.referral = referral
        self.state_tax = state_tax
        self.city_tax = city_tax
        self.county_tax = county_tax
        self.taxable_state = taxable_state
        self.taxable_city = taxable_city
        self.taxable_county = taxable_county
        self.client_ip = client_ip
        self.client_browser = client_browser
        self.printed = printed
        self.last_updated = last_updated
        self.last_updated_by = last_updated_by
        self.status = status
        self.is_shipped = is_shipped
        self.items = [OrderItem(**item) for item in items]
        self.tracking = [OrderTracking(**tracking) for tracking in tracking]
        self.history = [OrderHistory(**history) for history in history]
        self.packages = [OrderPackage(**package) for package in packages]

    def to_dict(self) -> dict:
        """Convert the Order object to a dictionary."""
        return {
            "id": self.id,
            "idcustomers": self.idcustomers,
            "distributor_id": self.distributor_id,
            "po_number": self.po_number,
            "so_number": self.so_number,
            "dist_order_id": self.dist_order_id,
            "invoice_number": self.invoice_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "company_name": self.company_name,
            "email": self.email,
            "street_address": self.street_address,
            "street_address_2": self.street_address_2,
            "city": self.city,
            "state": self.state,
            "zip": self.zip,
            "country": self.country,
            "subtotal": self.subtotal,
            "taxes": self.taxes,
            "shipping_cost": self.shipping_cost,
            "discount": self.discount,
            "total": self.total,
            "order_date": self.order_date,
            "timestamp": self.timestamp,
            "status_id": self.status_id,
            "payment_method": self.payment_method,
            "paypal_transaction_id": self.paypal_transaction_id,
            "paypal_capture_id": self.paypal_capture_id,
            "notes": self.notes,
            "sales_channel": self.sales_channel,
            "referral": self.referral,
            "state_tax": self.state_tax,
            "city_tax": self.city_tax,
            "county_tax": self.county_tax,
            "taxable_state": self.taxable_state,
            "taxable_city": self.taxable_city,
            "taxable_county": self.taxable_county,
            "client_ip": self.client_ip,
            "client_browser": self.client_browser,
            "printed": self.printed,
            "last_updated": self.last_updated,
            "last_updated_by": self.last_updated_by,
            "status": self.status,
            "is_shipped": self.is_shipped,
            "items": [item.to_dict() for item in self.items],
            "tracking": [tracking.to_dict() for tracking in self.tracking],
            "history": [history.to_dict() for history in self.history],
            "packages": [package.to_dict() for package in self.packages],
        }


class OrderItem:
    """Represents an order item."""

    def __init__(
        self,
        id,
        idorders,
        sku,
        title,
        price,
        qty,
        qty_filled,
        customization,
        cost,
        last_updated,
        last_updated_by,
        hidden,
    ):
        self.id = id
        self.idorders = idorders
        self.sku = sku
        self.title = title
        self.price = price
        self.qty = qty
        self.qty_filled = qty_filled
        self.customization = customization
        self.cost = cost
        self.last_updated = last_updated
        self.last_updated_by = last_updated_by
        self.hidden = hidden

    def to_dict(self) -> dict:
        """Convert the OrderItem object to a dictionary."""
        return {
            "id": self.id,
            "idorders": self.idorders,
            "sku": self.sku,
            "title": self.title,
            "price": self.price,
            "qty": self.qty,
            "qty_filled": self.qty_filled,
            "customization": self.customization,
            "cost": self.cost,
            "last_updated": self.last_updated,
            "last_updated_by": self.last_updated_by,
            "hidden": self.hidden,
        }


class OrderHistory:
    """Represents the history of an order."""

    def __init__(self, **kwargs):
        self.id = id
        if "order_id" in kwargs:
            self.order_id = kwargs["order_id"]
        elif "idorders" in kwargs:
            self.order_id = kwargs["idorders"]
        else:
            self.order_id = None
        self.status = kwargs.get("status", "")
        self.timestamp = kwargs.get("timestamp", "")
        self.updated_by = kwargs.get("updated_by", "")

    def to_dict(self) -> dict:
        """Convert the OrderHistory object to a dictionary."""
        return {
            "id": self.id,
            "order_id": self.order_id,
            "status": self.status,
            "timestamp": self.timestamp,
            "updated_by": self.updated_by,
        }


class OrderTracking:
    """Represents the tracking information for an order."""

    def __init__(
        self, id, idorders, courier, tracking_number, tracking_status, last_updated
    ):
        self.id = id
        self.idorders = idorders
        self.courier = courier
        self.tracking_number = tracking_number
        self.tracking_status = tracking_status
        self.last_updated = last_updated

    def to_dict(self) -> dict:
        """Convert the OrderTracking object to a dictionary."""
        return {
            "id": self.id,
            "idorders": self.idorders,
            "courier": self.courier,
            "tracking_number": self.tracking_number,
            "tracking_status": self.tracking_status,
            "last_updated": self.last_updated,
        }


class OrderPackage:
    """Represents a package in an order."""

    def __init__(
        self, id, idorders, lb, oz, length, width, height, shipped, order_status_id
    ):
        self.id = id
        self.idorders = idorders
        self.lb = lb
        self.oz = oz
        self.length = length
        self.width = width
        self.height = height
        self.shipped = shipped
        self.order_status_id = order_status_id

    def to_dict(self) -> dict:
        """Convert the OrderPackage object to a dictionary."""
        return {
            "id": self.id,
            "idorders": self.idorders,
            "lb": self.lb,
            "oz": self.oz,
            "length": self.length,
            "width": self.width,
            "height": self.height,
            "shipped": self.shipped,
            "order_status_id": self.order_status_id,
        }


class Orders:
    """Represents a list of orders."""

    def __init__(self, orders: list[Order]):
        self.orders: list[Order] = orders

    def to_dict(self) -> dict:
        """Convert the Orders object to a dictionary."""
        return {"orders": [order.to_dict() for order in self.orders]}

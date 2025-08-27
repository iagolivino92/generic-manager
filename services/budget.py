def calculate_budget(data, settings, translations):
    qty = float(data.get("quantity", 0))
    factory_price = float(data.get("factory_price", 0))
    silicone = float(data.get("silicone", 0))
    installation = float(data.get("installation", 0))
    transport_km = float(data.get("transport_km", 0))
    margin = float(data.get("margin", 0))

    discount_rate = settings["discount_rate"]
    iva_rate = settings["iva_rate"]
    transport_rate = settings["transport_rate"]

    price_with_discount = factory_price * (1 - discount_rate)
    total_installation = installation * qty
    transport_per_unit = transport_km * transport_rate

    total_cost = price_with_discount + silicone + installation + transport_per_unit
    price_without_iva = total_cost * (1 + margin)
    iva = price_without_iva * iva_rate
    final_price_with_iva = price_without_iva + iva
    total_with_iva = final_price_with_iva * qty

    return {
        translations.get('budget').get('fields').get('description'): data.get("description", ""),
        translations.get('budget').get('fields').get('quantity'): qty,
        translations.get('budget').get('fields').get('factory_price'): factory_price,
        translations.get('budget').get('fields').get('price_with_discount'): price_with_discount,
        translations.get('budget').get('fields').get('silicone'): silicone,
        translations.get('budget').get('fields').get('installation'): installation,
        translations.get('budget').get('fields').get('total_installation'): total_installation,
        translations.get('budget').get('fields').get('transportation_km'): transport_km,
        translations.get('budget').get('fields').get('transportation_price'): transport_per_unit,
        translations.get('budget').get('fields').get('total_cost'): total_cost,
        translations.get('budget').get('fields').get('margin'): margin,
        translations.get('budget').get('fields').get('price_without_iva'): price_without_iva,
        translations.get('budget').get('fields').get('iva'): iva,
        translations.get('budget').get('fields').get('final_price_with_iva'): final_price_with_iva,
        translations.get('budget').get('fields').get('total_with_iva'): total_with_iva
    }

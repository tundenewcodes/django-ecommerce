 try:
     cart  = json.loads(request.COOKIES['cart'])
except:
    cart = {}
        print('Cart', cart)        
        items = [] 
        order = {'get_cart_total_amt' : 0,'get_cart_total_qty' : 0,'shipping':False}
        cart_items = order['get_cart_total_qty']  
        for i in cart:
            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total_amt'] += total
            order['get_cart_total_qty'] += cart[i]['quantity'] 
            item = {
                'product' :{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                    
                },
                'quantity' : cart[i]['quantity'],
                'get_total': total
            }
            items.append(item)
        
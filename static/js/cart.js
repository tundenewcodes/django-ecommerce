const updateBtns = document.getElementsByClassName('update-cart')

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        const productId = this.dataset.product
        const action = this.dataset.action
        console.log({ productId, action })
        console.log('user:', user)
        if (user === 'AnonymousUser') {
            addCookieItem(productId, action)
        } else {
            updateUserOrder(productId, action)
        }
    })
}


const addCookieItem = (productId, action) => {
    console.log('not logged in')
    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = { 'quantity': 1 }
        } else {
            cart[productId]['quantity'] += 1
        }
        //location.reload()
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1
        if (cart[productId]['quantity'] < 0) {
            delete cart[productId]
        }
        //location.reload()

    }

    console.log('cart : ', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"

}

const updateUserOrder = (productId, action) => {
    console.log('user is logged in sending data')
    let url = '/update-item/'
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/Json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ productId, action })
        })
        .then(response => {
            return response.json()
        })
        .then(data => {
            console.log({ data })
            location.reload()
        })
}
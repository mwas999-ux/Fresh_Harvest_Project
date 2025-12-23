// Cart functionality
class ShoppingCart {
    constructor() {
        this.cart = JSON.parse(localStorage.getItem('cart')) || {};
        this.updateCartCount();
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Add to cart buttons
        document.querySelectorAll('.add-to-cart').forEach(button => {
            button.addEventListener('click', (e) => {
                const id = e.target.dataset.id;
                const name = e.target.dataset.name;
                const price = parseFloat(e.target.dataset.price);
                this.addItem(id, name, price);
            });
        });

        // Cart modal
        const modal = document.getElementById('cart-modal');
        const cartLink = document.getElementById('cart-link');
        const closeBtn = document.querySelector('.close');

        if (cartLink) {
            cartLink.addEventListener('click', (e) => {
                e.preventDefault();
                this.showCart();
                modal.style.display = 'block';
            });
        }

        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                modal.style.display = 'none';
            });
        }

        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    }

    addItem(id, name, price) {
        if (this.cart[id]) {
            this.cart[id].quantity += 1;
        } else {
            this.cart[id] = { name, price, quantity: 1 };
        }
        this.saveCart();
        this.updateCartCount();
        this.showNotification(`${name} added to cart!`);
    }

    removeItem(id) {
        delete this.cart[id];
        this.saveCart();
        this.updateCartCount();
        this.showCart();
    }

    updateQuantity(id, quantity) {
        if (quantity <= 0) {
            this.removeItem(id);
        } else {
            this.cart[id].quantity = quantity;
            this.saveCart();
            this.showCart();
        }
    }

    saveCart() {
        localStorage.setItem('cart', JSON.stringify(this.cart));
    }

    updateCartCount() {
        const count = Object.values(this.cart).reduce((sum, item) => sum + item.quantity, 0);
        const countElement = document.getElementById('cart-count');
        if (countElement) {
            countElement.textContent = count;
        }
    }

    showCart() {
        const cartItems = document.getElementById('cart-items');
        if (!cartItems) return;

        let html = '';
        let total = 0;

        for (const [id, item] of Object.entries(this.cart)) {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;

            html += `
                <div class="cart-item">
                    <span>${item.name}</span>
                    <div>
                        <button onclick="cart.updateQuantity('${id}', ${item.quantity - 1})">-</button>
                        <span>${item.quantity}</span>
                        <button onclick="cart.updateQuantity('${id}', ${item.quantity + 1})">+</button>
                        <span>KSh ${itemTotal.toFixed(2)}</span>
                        <button onclick="cart.removeItem('${id}')">Remove</button>
                    </div>
                </div>
            `;
        }

        cartItems.innerHTML = html || '<p>Your cart is empty</p>';
        document.getElementById('cart-total').textContent = total.toFixed(2);
    }

    showNotification(message) {
        // Simple notification (you can enhance this)
        const notification = document.createElement('div');
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #2d6a4f;
            color: white;
            padding: 1rem 2rem;
            border-radius: 5px;
            z-index: 10000;
        `;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 2000);
    }
}

// Initialize cart
const cart = new ShoppingCart();
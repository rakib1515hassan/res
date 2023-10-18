console.log("Sanity check!");



// get Stripe Publishable key
const product = document.getElementsByClassName("product");

product[0].addEventListener("click", () => {
    var url = product[0].getAttribute('data_url')
    fetch("/checkout/config")
    .then((result) => { return result.json(); })
    .then((data) => {
        //Initialize Stripe.js
        const stripe = Stripe(data.publicKey)
            //Get Checkout Session ID
            fetch("/checkout/create-checkout-session?product=" + url)
            .then((result) => {return result.json(); })
            .then((data) => {
                console.log(data);
                //Redirect to Stripe Checkout
                return stripe.redirectToCheckout({sessionId: data.sessionId})
            })
            .then((res) => {
                console.log(res);
            });
        });
});


product[1].addEventListener("click", () => {
    var url = product[1].getAttribute('data_url')
    fetch("/checkout/config")
    .then((result) => { return result.json(); })
    .then((data) => {
        //Initialize Stripe.js
        const stripe = Stripe(data.publicKey)
            //Get Checkout Session ID
            fetch("/checkout/create-checkout-session?product=" + url)
            .then((result) => {return result.json(); })
            .then((data) => {
                console.log(data);
                //Redirect to Stripe Checkout
                return stripe.redirectToCheckout({sessionId: data.sessionId})
            })
            .then((res) => {
                console.log(res);
            });
        });
});


product[2].addEventListener("click", () => {
    var url = product[2].getAttribute('data_url')
    fetch("/checkout/config")
    .then((result) => { return result.json(); })
    .then((data) => {
        //Initialize Stripe.js
        const stripe = Stripe(data.publicKey)
            //Get Checkout Session ID
            fetch("/checkout/create-checkout-session?product=" + url)
            .then((result) => {return result.json(); })
            .then((data) => {
                console.log(data);
                //Redirect to Stripe Checkout
                return stripe.redirectToCheckout({sessionId: data.sessionId})
            })
            .then((res) => {
                console.log(res);
            });
        });
});
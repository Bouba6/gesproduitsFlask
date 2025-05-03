document.getElementById("search").addEventListener("input", function (event) {
    event.preventDefault();
    console.log("hello");

    async function searchProduct() {
        let search = document.getElementById("search").value;
        let url = search ? `/search/${search}` : '';  

        
        fetch(url)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                let products = document.getElementById("products");
                products.innerHTML = "";  
               
                if (data.length === 0) {
                    products.innerHTML = "<p>Aucun produit trouvé.</p>";
                    return;
                }

              
                data.forEach(product => {
                    products.innerHTML += `
                        <div class="flex flex-col w-1/3">
                            <div class="bg-white shadow-md w-auto rounded px-8 pt-6 pb-8 mb-4">
                                <img class="w-full h-96 object-cover" src="/static/images/${product.image}" alt="Image de ${product.name}" />
                                <div class="mb-4">
                                    <label class="block text-gray-700 text-sm font-bold mb-2">Name</label>
                                    <p class="text-gray-700 text-base">${product.name}</p>
                                </div>
                                <div class="mb-4">
                                    <label class="block text-gray-700 text-sm font-bold mb-2">Price</label>
                                    <p class="text-gray-700 text-base">${product.price}</p>
                                </div>
                                <div class="mb-4">
                                    <label class="block text-gray-700 text-sm font-bold mb-2">Description</label>
                                    <p class="text-gray-700 text-base">${product.description}</p>
                                </div>
                                <div class="mb-4">
                                    <label class="block text-gray-700 text-sm font-bold mb-2">Quantity</label>
                                    <p class="text-gray-700 text-base">${product.qte}</p>
                                </div>
                            </div>
                        </div>`;
                });
            })
            .catch(error => {
                console.error("Erreur lors de la récupération des produits :", error);
            });
    }

    searchProduct();
});

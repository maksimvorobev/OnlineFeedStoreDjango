$(document).ready(function () {

    // Оповещение от ajax
    var successMessage = $("#jq-notification");



    // Обработчик собыития клика по кнопке добавить в корзину
    $(document).on("click", ".add-to-cart", function (e) {
        e.preventDefault();

        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);
        var product_id = $(this).data("product-id");
        var add_to_cart_url = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {

                successMessage.html(data.message);
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 3000);

                cartCount++;
                goodsInCartCount.text(cartCount);

                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });



    // Обработчик собыития клика по кнопке удалить товар из корзины
    $(document).on("click", ".remove-from-cart", function (e) {
        e.preventDefault();

        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);
        var cart_id = $(this).data("cart-id");
        var remove_from_cart = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {

                successMessage.html(data.message);
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 3000);

                cartCount -= data.quantity_deleted;
                goodsInCartCount.text(cartCount);

                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

                if (data.redirect_to_home)
                    window.location.href = '/';

            },

            error: function (data) {
                console.log("Ошибка при удалении товара из корзины");
            },
        });
    });



    // Обработчики событий клика по кнопкам + - количества товара 
    // Обработчик события для уменьшения значения
    $(document).on("click", ".decrement", function () {
        var url = $(this).data("cart-change-url");
        var cartID = $(this).data("cart-id");
        var $input = $(this).closest('.input-group').find('.number');
        var currentValue = parseInt($input.val());

        if (currentValue > 1) {
            $input.val(currentValue - 1);
            updateCart(cartID, currentValue - 1, -1, url);
        }
    });

    // Обработчик события для увеличения значения
    $(document).on("click", ".increment", function () {
        var url = $(this).data("cart-change-url");
        var cartID = $(this).data("cart-id");
        var $input = $(this).closest('.input-group').find('.number');
        var currentValue = parseInt($input.val());

        $input.val(currentValue + 1);

        updateCart(cartID, currentValue + 1, 1, url);
    });

    // Обновляет html корзины
    function updateCart(cartID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {

                successMessage.html(data.message);
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 3000);

                var goodsInCartCount = $("#goods-in-cart-count");
                var cartCount = parseInt(goodsInCartCount.text() || 0);
                cartCount += change;
                goodsInCartCount.text(cartCount);

                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

                if (data.redirect_to_home)
                    window.location.href = '/';

            },
            error: function (data) {
                console.log("Ошибка при изменении кол-ва товара в корзине");
            },
        });
    }



    // Обратная связь
    // Обработчик события клика по кнопке Обратная связь
    $(document).on("click", ".header__feedback-btn", function (e) {
        e.preventDefault();
    
        var url = $(this).data("feedback-url");
    
        $.ajax({
            type: "GET",
            url: url,
            success: function (data) {
                var popupFeedbackContainer = $("#popup-feedback-container");
                popupFeedbackContainer.html(data.feedback_html);
            },
            error: function () {
                console.log("Ошибка загрузки формы обратной связи");
            }
        });
    });
    
    // Обработчик события клика по кнопке Отправить сообщение
    $(document).on("submit", "#feedback-form", function (e) {
        e.preventDefault();
        $(".feedback-btn").attr("disabled", true);

        var form = $(this);
        var url = form.attr('action');
    
        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(),
            success: function (data) {
                if (data.success) {
                    location.reload();

                } else {
                    var popupFeedbackContainer = $("#popup-feedback-container");
                    popupFeedbackContainer.html(data.feedback_html);
                }
            },
            error: function () {
                console.log("Ошибка отправки формы обратной связи");
            }
        });
    });



    // Уведомления на сайте
    var notification = $('#notification');
    if (notification.length > 0) {
        setTimeout(function () {
            notification.hide();
        }, 5000);
    }



    // Обработчик события кнопки Сменить фото профиля
    $('.user-data-form__input-img').on('change', function () {
        let file = this.files[0];
        $(this).next().html(file.name);
    });



    // Обработчик события клика по кнопке отображения заказов в профиле
    $('.orders-tab__btn').click(function () {
        $(this).toggleClass('active');
        $(this).siblings('.orders-tab__content').slideToggle();
    });



    // Обработчик события радиокнопки выбора способа доставки
    $("input[name='requires_delivery']").change(function () {
        var selectedValue = $(this).val();
        if (selectedValue === "1") {
            $("#deliveryAddressField").show();
        } else {
            $("#deliveryAddressField").hide();
        }
    });



    // Нажатие на ссылки раскрывающихся меню на смартфонах и планшетах
    // Обработчик события клика по ссылке раскрывающегося меню на смартфонах и планшетах
    $('.menu__list-item-drop-link').on('click', function (event) {
        var windowWidth = $(window).width();
        if (windowWidth < 1180) {
            event.preventDefault();
        }
    });

    $('.menu__list-item_drop').on('click', function (event) {
        var windowWidth = $(window).width();
        if (windowWidth < 1180) {
            var submenu = $(this).find('.menu__sublist');
            if (submenu.hasClass('menu__sublist_open')) {
                submenu.slideUp().removeClass('menu__sublist_open');
            } else {
                $('.menu__sublist--open').slideUp().removeClass('menu__sublist_open');
                submenu.slideDown().addClass('menu__sublist_open');
            }
        }
        event.stopPropagation();
    });

    $('.menu__list').on('click', function (event) {
        $('.menu__sublist_open').slideUp().removeClass('menu__sublist_open');
    });
});
const closeNotifButton = document.querySelectorAll(".notif__btn-close");

closeNotifButton.forEach(function (element) {
  element.addEventListener("click", closeNotification);
});

function closeNotification(evt) {
  const buttonTarget = evt.currentTarget;
  const notification = buttonTarget.closest('.notif__inner');
  notification.style.display = "none";
}


const tabItem = document.querySelectorAll(".tabs__btn-item");
const tabContent = document.querySelectorAll(".tabs__content-item");

tabItem.forEach(function (element) {
  element.addEventListener("click", open);
});

function open(evt) {
  const tabTarger = evt.currentTarget;
  const button = tabTarger.dataset.button;

  tabItem.forEach(function (item) {
    item.classList.remove("tabs__btn-item_active");
  });
  tabTarger.classList.add("tabs__btn-item_active");

  tabContent.forEach(function (item) {
    item.classList.remove("tabs__content-item_active");
  });
  document
    .querySelector(`#${button}`)
    .classList.add("tabs__content-item_active");
}


const menuBtn = document.querySelector(".menu__btn");
const menuList = document.querySelector(".menu__list");

menuBtn.addEventListener("click", () => {
  menuBtn.classList.toggle("menu__btn_active");
  menuList.classList.toggle("menu__list_active");
});
window.addEventListener("click", (e) => {
  const target = e.target;
  if (!target.closest(".menu__list") && !target.closest(".menu__btn")) {
    menuList.classList.remove("menu__list_active");
    menuBtn.classList.remove("menu__btn_active");
  }
});

const scrollController = {
  scrollPosition: 0,
  disabledScroll() {
    scrollController.scrollPosition = window.scrollY;
    document.body.style.cssText = `
      overflow: hidden;
      position: fixed;
      top: -${scrollController.scrollPosition}px;
      left 0;
      height: 100vh;
      width: 100vw;
      padding-right: ${window.innerWidth - document.body.offsetWidth}px;
    `;
  },
  enabledScroll() {
    document.body.style.cssText = "";
    window.scroll({ top: scrollController.scrollPosition });
  },
};

const popUpController = ({ popup, btnOpen, btnClose, time = 300 }) => {
  const buttonElems = document.querySelectorAll(btnOpen);
  const popUpElem = document.querySelector(popup);

  popUpElem.style.cssText = `
    display: flex;
    visibility: hidden;
    opacity: 0;
    transition: opacity ${time}ms ease-in-out;
    `;

  const closePopUp = (event) => {
    const target = event.target;

    if (
      target === popUpElem ||
      (btnClose && target.closest(btnClose)) ||
      event.code === "Escape"
    ) {
      popUpElem.style.opacity = 0;

      setTimeout(() => {
        popUpElem.style.visibility = "hidden";
        scrollController.enabledScroll();
      }, time);

      window.removeEventListener("keydown", closePopUp);
    }
  };

  const openPopUp = () => {
    popUpElem.style.visibility = "visible";
    popUpElem.style.opacity = 1;
    window.addEventListener("keydown", closePopUp);
    scrollController.disabledScroll();
  };

  buttonElems.forEach((btn) => {
    btn.addEventListener("click", openPopUp);
  });

  popUpElem.addEventListener("click", closePopUp);
};

popUpController({
  popup: ".popup",
  btnOpen: ".popup__open",
  btnClose: ".popup__close",
});

popUpController({
  popup: ".cart_popup",
  btnOpen: ".cart_popup__open",
  btnClose: ".cart_popup__close",
});

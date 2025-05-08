// Mobile Menu Toggle
document.getElementById("mobile-menu-button")?.addEventListener("click", function () {
    const menu = document.getElementById("mobile-menu");
    menu.classList.toggle("open");
  });
  
  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
  
      // Close mobile menu if open
      const mobileMenu = document.getElementById('mobile-menu');
      if (mobileMenu && mobileMenu.classList.contains('open')) {
        mobileMenu.classList.remove('open');
      }
  
      const targetId = this.getAttribute('href');
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        window.scrollTo({
          top: targetElement.offsetTop - 80,
          behavior: 'smooth'
        });
      }
    });
  });
  
  // Highlight active nav link on scroll
  const sections = document.querySelectorAll('section');
  const navLinks = document.querySelectorAll('.nav-link');
  
  window.addEventListener('scroll', function () {
    let current = '';
    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      if (pageYOffset >= (sectionTop - 100)) {
        current = section.getAttribute('id');
      }
    });
  
    navLinks.forEach(link => {
      link.classList.remove('active-nav');
      if (link.getAttribute('href') === `#${current}`) {
        link.classList.add('active-nav');
      }
    });
  });
  
  // Back to Top Button
  const backToTopButton = document.getElementById('back-to-top');
  window.addEventListener('scroll', function () {
    if (window.pageYOffset > 300) {
      backToTopButton.classList.add('visible');
    } else {
      backToTopButton.classList.remove('visible');
    }
  });
  backToTopButton.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
  
  // Disable parallax on mobile devices
  function checkParallax() {
    const parallaxElements = document.querySelectorAll('.parallax');
    if (window.innerWidth < 768) {
      parallaxElements.forEach(el => el.style.backgroundAttachment = 'scroll');
    } else {
      parallaxElements.forEach(el => el.style.backgroundAttachment = 'fixed');
    }
  }
  window.addEventListener('resize', checkParallax);
  checkParallax();
  
  // Initialize Flatpickr
  document.querySelectorAll(".flatpickr-input").forEach(input => {
    flatpickr(input, {
      altInput: true,
      altFormat: "d.m.Y",
      dateFormat: "Y-m-d",
      minDate: "today"
    });
  });
  
  // Open/Close Booking Modal
  // document.getElementById("openBookingModal")?.addEventListener("click", () => {
  //   document.getElementById("bookingModal").classList.remove("hidden");
  // });
  // document.getElementById("openBookingModalMobile")?.addEventListener("click", () => {
  //   document.getElementById("bookingModal").classList.remove("hidden");
  // });
  document.getElementById("openBookingModalFromAccommodation")?.addEventListener("click", () => {
    document.getElementById("bookingModal").classList.remove("hidden");
  });
  document.getElementById("closeModal")?.addEventListener("click", () => {
    document.getElementById("bookingModal").classList.add("hidden");
  });
  window.addEventListener("click", (e) => {
    const modal = document.getElementById("bookingModal");
    if (e.target === modal) {
      modal.classList.add("hidden");
    }
  });
  
  // Инициализация календарей в модальном окне
const checkinModal = document.getElementById("checkinModal");
const checkoutModal = document.getElementById("checkoutModal");

if (checkinModal && checkoutModal) {
  flatpickr(checkinModal, {
    altInput: true,
    altFormat: "d.m.Y",
    dateFormat: "Y-m-d",
    minDate: "today",
    onChange: function(selectedDates, dateStr, instance) {
      if (selectedDates.length > 0) {
        checkoutModal._flatpickr.set("minDate", dateStr);
      }
    }
  });

  flatpickr(checkoutModal, {
    altInput: true,
    altFormat: "d.m.Y",
    dateFormat: "Y-m-d",
    minDate: "today"
  });
}


document.addEventListener("DOMContentLoaded", function () {
  fetch("https://chernoyarka-project-backend.onrender.com/api/booked-dates/")
      .then(res => res.json())
      .then(data => {
          const disabledDates = data.booked_dates || [];

          flatpickr("#checkin", {
              altInput: true,
              altFormat: "d.m.Y",
              dateFormat: "Y-m-d",
              minDate: "today",
              disable: disabledDates
          });

          flatpickr("#checkout", {
              altInput: true,
              altFormat: "d.m.Y",
              dateFormat: "Y-m-d",
              minDate: "today",
              disable: disabledDates
          });
      });
});

document.getElementById("smartBookingForm")?.addEventListener("submit", async function (e) {
  e.preventDefault();

  const form = e.target;
  const roomId = form.dataset.roomId;

  const name = document.getElementById("fullName2").value.trim();
  const phone = document.getElementById("phone2").value.trim();
  const email = document.getElementById("email2").value.trim();
  const checkIn = document.getElementById("checkinModal").value;
  const checkOut = document.getElementById("checkoutModal").value;
  const adults = parseInt(document.getElementById("adults").value);
  const children = parseInt(document.getElementById("children").value);
  const note = document.getElementById("notes").value.trim();

  // === Валидация обязательных полей
  if (!name || !phone || !email || !checkIn || !checkOut) {
    alert("Пожалуйста, заполните все обязательные поля.");
    return;
  }

  // === Валидация email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    alert("Некорректный email.");
    return;
  }

  // === Валидация телефона
  if (phone.length < 6) {
    alert("Пожалуйста, введите корректный номер телефона.");
    return;
  }

  // === Проверка дат
  const today = new Date().setHours(0,0,0,0);
  const checkInDate = new Date(checkIn).setHours(0,0,0,0);
  const checkOutDate = new Date(checkOut).setHours(0,0,0,0);

  if (checkInDate < today) {
    alert("Нельзя бронировать на прошедшую дату.");
    return;
  }

  if (checkOutDate <= checkInDate) {
    alert("Дата выезда должна быть позже даты заезда.");
    return;
  }

  // === SQL-инъекции (грубый фильтр)
  const forbiddenPattern = /('|--|;|\/\*|\*\/|select|union|insert|drop|update|delete|alter|create|exec|xp_cmdshell|or\s+1=1)/i;

  if (
    forbiddenPattern.test(name) ||
    forbiddenPattern.test(phone) ||
    forbiddenPattern.test(email) ||
    forbiddenPattern.test(note)
  ) {
    alert("Ввод содержит недопустимые символы. Пожалуйста, удалите подозрительный текст.");
    return;
  }

  // === Отправка
  const payload = {
    name,
    phone,
    email,
    check_in: checkIn,
    check_out: checkOut,
    adults,
    children,
    note,
    room: roomId ? parseInt(roomId) : null
  };

  const res = await fetch("https://chernoyarka-project-backend.onrender.com/api/rooms/book/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (res.ok) {
    alert("Бронирование успешно отправлено!");
    this.reset();
    document.getElementById("bookingModal").classList.add("hidden");
  } else {
    const err = await res.json();
    alert("Ошибка: " + JSON.stringify(err));
  }
});



document.getElementById("openBookingModalFromHero")?.addEventListener("click", async function (e) {
  e.preventDefault();

  const checkin = document.getElementById("checkin").value;
  const checkout = document.getElementById("checkout").value;
  const adults = document.getElementById("adults").value || 1;
  const children = document.getElementById("children").value || 0;

  if (!checkin || !checkout) {
    alert("Пожалуйста, выберите даты.");
    return;
  }

  const query = `https://chernoyarka-project-backend.onrender.com/api/rooms/available/?check_in=${checkin}&check_out=${checkout}&adults=${adults}&children=${children}`;

  try {
    const res = await fetch(query);
    const rooms = await res.json();

    const container = document.getElementById("availableRooms");
    container.innerHTML = "";

    if (rooms.length === 0) {
      container.innerHTML = "<p>Нет доступных номеров на выбранные даты.</p>";
      return;
    }

    rooms.forEach(room => {
      const card = document.createElement("div");
      card.className = "room-card p-4 border rounded shadow text-center max-w-xl mx-auto bg-white flex flex-col justify-between";

      const checkinDate = new Date(checkin);
      const checkoutDate = new Date(checkout);

      if (new Date(checkout) <= new Date(checkin)) {
        console.warn("Некорректные даты: выезд раньше заезда");
        return; 
      }      

      const nights = Math.ceil((checkoutDate - checkinDate) / (1000 * 60 * 60 * 24));
      const guests = parseInt(adults) + parseInt(children);
      const totalPrice = guests * nights * room.price_per_night;
    
      card.innerHTML = `
        <h3 class="text-xl font-bold mb-2">${room.name}</h3>
        <p class="mb-1 text-sm text-gray-600">${room.description}</p>
        <p>Вместимость: ${room.capacity}</p>
        <p>Цена за человека: ${room.price_per_night} KZT</p>
        <p>Гостей: ${guests}, Ночей: ${nights}</p>
        <p class="font-semibold text-lg mt-1">Итого: ${totalPrice} KZT</p>
        <button class="btn btn-primary mt-3" data-room-id="${room.id}">
          Забронировать
        </button>
      `;
    
      container.appendChild(card);
    
      card.querySelector("button").addEventListener("click", () => {
        document.getElementById("bookingModal").classList.remove("hidden");
        document.getElementById("checkinModal").value = checkin;
        document.getElementById("checkoutModal").value = checkout;
        document.getElementById("adults").value = adults;
        document.getElementById("children").value = children;
    
        document.getElementById("smartBookingForm").dataset.roomId = room.id;
      });
    });
    

  } catch (err) {
    console.error("Ошибка при загрузке номеров:", err);
    alert("Ошибка загрузки номеров");
  }
});

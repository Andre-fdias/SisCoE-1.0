function getGreeting() {
    const hours = new Date().getHours();
    if (hours < 12) {
        return "Bom dia";
    } else if (hours < 18) {
        return "Boa tarde";
    } else {
        return "Boa noite";
    }
}

function getWeekdayName(date) {
    const days = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'];
    return days[date.getDay()];
}

function updateClock() {
    const now = new Date();
    const greeting = getGreeting();
    const weekday = getWeekdayName(now);
    const date = now.toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' });
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');
    const timeString = `${hours}:${minutes}:${seconds}`;
    document.getElementById('greeting').textContent = greeting;
    document.getElementById('date').textContent = `${weekday}, ${date}`;
    document.getElementById('time').textContent = timeString;
}

setInterval(updateClock, 1000); // Atualiza o relógio a cada segundo
updateClock(); // Atualiza o relógio imediatamente ao carregar a página

function toggleTheme() {
    const main = document.main;
    body.classList.toggle('dark-mode');

    // Salvar a preferência do usuário no localStorage
    if (main.classList.contains('dark-mode')) {
        localStorage.setItem('theme', 'dark');
    } else {
        localStorage.setItem('theme', 'light');
    }
}

// Aplicar o tema salvo no localStorage
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
    }

    const themeToggle = document.getElementById('theme-toggle');
    themeToggle.addEventListener('click', toggleTheme);

    // Código existente
    fetchLocationAndWeather();
    document.querySelectorAll('.dropdown-submenu .dropdown-toggle').forEach(function(element) {
        element.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            let nextElement = element.nextElementSibling;
            if (nextElement && nextElement.classList.contains('dropdown-menu')) {
                nextElement.classList.toggle('show');
            }
        });
    });
});


document.getElementById('date').innerHTML = new Date().toLocaleDateString();
setInterval(() => {
    document.getElementById('time').innerHTML = new Date().toLocaleTimeString();
}, 1000);

document.addEventListener('DOMContentLoaded', () => {
    // Código existente
    fetchLocationAndWeather();
    document.querySelectorAll('.dropdown-submenu .dropdown-toggle').forEach(function(element) {
        element.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            let nextElement = element.nextElementSibling;
            if (nextElement && nextElement.classList.contains('dropdown-menu')) {
                nextElement.classList.toggle('show');
            }
        });
    });

    // Adicionando funcionalidade para os dropdowns da sidebar
    document.querySelectorAll('#sidebar .dropdown-toggle').forEach(function(element) {
        element.addEventListener('click', function(e) {
            e.preventDefault();
            let nextElement = element.nextElementSibling;
            if (nextElement && nextElement.classList.contains('collapse')) {
                nextElement.classList.toggle('show');
            }
        });
    });
});

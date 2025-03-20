function showNotification(message, type = 'success', redirectUrl = null, delay = 3000) {
    // Создаем элемент для уведомления
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button class="close-btn">OK</button>
    `;

    // Добавляем уведомление в контейнер
    const container = document.getElementById('notification-container');
    if (!container) {
        console.error("Контейнер для уведомлений не найден!");
        return;
    }
    container.appendChild(notification);

    // Показываем уведомление
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);

    // Закрытие уведомления при нажатии на кнопку "OK"
    const closeButton = notification.querySelector('.close-btn');
    closeButton.addEventListener('click', () => {
        notification.classList.remove('show');

        setTimeout(() => {
            container.removeChild(notification);
        }, 300); // Время должно совпадать с длительностью CSS-перехода

        // Редирект при нажатии на кнопку
        if (redirectUrl) {
            window.location.href = redirectUrl;
        }
    });

    // Автоматическое скрытие уведомления через заданное время
    setTimeout(() => {
        notification.classList.remove('show');

        setTimeout(() => {
            container.removeChild(notification);
        }, 300); // Время должно совпадать с длительностью CSS-перехода

        // Редирект после автоматического закрытия
        if (redirectUrl) {
            window.location.href = redirectUrl;
        }
    }, delay); // Используем переданную задержку
}
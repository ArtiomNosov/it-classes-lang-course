function showNotification(message, type = 'success') {
    // Создаем элемент для уведомления
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button class="close-btn">OK</button>
    `;

    // Добавляем уведомление в контейнер
    const container = document.getElementById('notification-container');
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
    });

    // Автоматически скрываем уведомление через 3 секунды
    setTimeout(() => {
        notification.classList.remove('show');

        setTimeout(() => {
            container.removeChild(notification);
        }, 300);
    }, 3000);
}
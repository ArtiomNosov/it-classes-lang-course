document.addEventListener('DOMContentLoaded', () => {
    const courseButton = document.getElementById('course-button');
    const forumButton = document.getElementById('forum-button');
    forumButton.classList.add('active');
    courseButton.classList.remove('active');
    forumButton.addEventListener('click', () => {
        forumButton.classList.add('active');
        courseButton.classList.remove('active');
        // Можно добавить переход на страницу курса
    });

    courseButton.addEventListener('click', () => {
        courseButton.classList.add('active');
        forumButton.classList.remove('active');
        // Переход на страницу форума
        window.location.href = '/'; // Замените на нужный URL
    });
});

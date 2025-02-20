document.addEventListener('DOMContentLoaded', () => {
    const courseButton = document.getElementById('course-button');
    const forumButton = document.getElementById('forum-button');
    courseButton.classList.add('active');
    forumButton.classList.remove('active');
    
    courseButton.addEventListener('click', () => {
        courseButton.classList.add('active');
        forumButton.classList.remove('active');
        window.location.href = '/';
        // Можно добавить переход на страницу курса
    });

    forumButton.addEventListener('click', () => {
        forumButton.classList.add('active');
        courseButton.classList.remove('active');
        // Переход на страницу форума
        window.location.href = 'forum'; // Замените на нужный URL
    });
});

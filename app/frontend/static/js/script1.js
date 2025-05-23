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
        window.location.href = '/forum'; // Замените на нужный URL
    });

    const tabEditor = document.getElementById('tab-editor');
    const tabOutput = document.getElementById('tab-output');

    tabOutput.addEventListener('click', () => {
        tabOutput.classList.add('active');
        tabEditor.classList.remove('active');
    });

    tabEditor.addEventListener('click', () => {
        tabEditor.classList.add('active');
        tabOutput.classList.remove('active');
    });
});

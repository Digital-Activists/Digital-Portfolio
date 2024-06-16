document.querySelector('form').classList.add('search');

// Создаем новый div-элемент
const formDiv = document.createElement('div');
formDiv.classList.add('form-wrapper');

// Выбираем форму
const form = document.querySelector('form');

// Создаем массив из элементов формы, исключая первый и последний элементы
const formElements = Array.prototype.slice.call(form.children, 1, -1);

// Помещаем элементы формы в новый div
formElements.forEach(element => formDiv.appendChild(element));

// Добавляем новый div перед кнопками submit
form.insertBefore(formDiv, form.lastChild);

const showParamsBtn = document.querySelector('#show-params-btn');
const formWrapper = document.querySelector('.form-wrapper');
formWrapper.style.display = 'none';
showParamsBtn.addEventListener('click', () => {
    if (formWrapper.style.display === 'none') {
        formWrapper.style.display = 'flex';
    } else {
        formWrapper.style.display = 'none';
    }
});
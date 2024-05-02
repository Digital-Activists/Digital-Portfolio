function openForm(social_network) {
    document.getElementById("socialModal").style.display = "block";
    document.getElementById(social_network).value = social_network;
}

function closeForm() {
    document.getElementById("socialModal").style.display = "none";
}

document.querySelector('#demoModalStart').addEventListener('click', function () {
    document.querySelector('#socialModal').style.display = 'flex';
});
// Закрытие модального окна
document.querySelector('#demoModalStart').addEventListener('click', function () {
    document.querySelector('#socialModal').style.display = 'none';
});

// document.getElementById("add_social-network-form").addEventListener('submit', function (event) {
//     event.preventDefault();
//
//     // Создаем новый объект FormData и передаем в него нашу форму
//     const formData = new FormData(event.target);
//
//     // Отправляем данные формы на сервер с использованием fetch
//     fetch('submit-social-network-form', {
//         method: 'POST',
//         body: formData
//     })
//         .then(response => response.json())
//         .then(data => console.log(data))
//         .catch(error => console.error('Error:', error));
// });
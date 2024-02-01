const editUsernameInput = document.getElementById('editUsernameInput');
const submitEditUsername = document.getElementById('submitEditUsername');

editUsernameInput.addEventListener('input', () => {
    if (editUsernameInput.value.trim() !== '') {
        submitEditUsername.style.display = 'block';
    } else {
        submitEditUsername.style.display = 'none';
    }
});


const editPasswordInput = document.getElementById('editPasswordInput');
const submitEditPassword = document.getElementById('submitEditPassword');

editPasswordInput.addEventListener('input', () => {
    if (editPasswordInput.value.trim() !== '') {
        submitEditPassword.style.display = 'block';
    } else {
        submitEditPassword.style.display = 'none';
    }
});


const editAuthInput = document.getElementById('editAuthInput');
const submitEditAuth = document.getElementById('submitEditAuth');

editAuthInput.addEventListener('input', () => {
    if (editAuthInput.value.trim() !== '') {
        submitEditAuth.style.display = 'block';
    } else {
        submitEditAuth.style.display = 'none';
    }
});


const editStatusInput = document.getElementById('editStatusInput');
const submitEditStatus = document.getElementById('submitEditStatus');

editStatusInput.addEventListener('input', () => {
    if (editStatusInput.value.trim() !== '') {
        submitEditStatus.style.display = 'block';
    } else {
        submitEditStatus.style.display = 'none';
    }
});
document.querySelector('.form__file').onchange = function () {
    console.log(this.files);
    document.querySelector('.form__filename').textContent = this.files[0].name;
}

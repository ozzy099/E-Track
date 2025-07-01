
const urlParams = new URLSearchParams(window.location.search);
const mode = urlParams.get('mode');
const resource = urlParams.get('resource');
if (mode === 'edit') {
  document.getElementById('header').textContent = `Edit ${resource}`;
  document.getElementById('passwordField').style.display = 'none';
}

// document.addEventListener("DOMContentLoaded", () => {
//   const addUserform = document.getElementById('addUserForm');
//   const addItemCategoryForm = document.getElementById('addItemCategoryForm');

// });
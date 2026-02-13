document.addEventListener('DOMContentLoaded', function() {

  const uploadForm = document.querySelector('form[action*="upload"]');
  if (uploadForm) {
    uploadForm.addEventListener('submit', function(e) {
      const titleInput = this.querySelector('input[name="title"]');
      const fileInput = this.querySelector('input[name="file"]');

      if (!titleInput.value.trim()) {
        e.preventDefault();
        alert('Por favor, preencha o título do documento.');
        titleInput.focus();
        return false;
      }

      if (!fileInput.files || fileInput.files.length === 0) {
        e.preventDefault();
        alert('Por favor, selecione um arquivo.');
        fileInput.focus();
        return false;
      }

      const fileName = fileInput.files[0].name.toLowerCase();
      const validExtensions = ['.pdf', '.jpg', '.jpeg', '.png'];
      const hasValidExtension = validExtensions.some(ext => fileName.endsWith(ext));

      if (!hasValidExtension) {
        e.preventDefault();
        alert('Formato de arquivo inválido. Use PDF, JPG ou PNG.');
        fileInput.value = '';
        return false;
      }

      const maxSize = 20 * 1024 * 1024;
      if (fileInput.files[0].size > maxSize) {
        e.preventDefault();
        alert('Arquivo muito grande. O tamanho máximo é 20MB.');
        fileInput.value = '';
        return false;
      }
    });
  }

  const commentForms = document.querySelectorAll('form[action*="comments"]');
  commentForms.forEach(form => {
    form.addEventListener('submit', function(e) {
      const contentInput = this.querySelector('textarea[name="content"]');

      if (!contentInput.value.trim()) {
        e.preventDefault();
        alert('Por favor, digite um comentário.');
        contentInput.focus();
        return false;
      }
    });
  });

  const fileInputs = document.querySelectorAll('input[type="file"]');
  fileInputs.forEach(input => {
    input.addEventListener('change', function() {
      if (this.files && this.files.length > 0) {
        const fileName = this.files[0].name;
        const fileSize = (this.files[0].size / 1024 / 1024).toFixed(2);
        console.log(`Arquivo selecionado: ${fileName} (${fileSize} MB)`);
      }
    });
  });

});

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('partnerSearch').addEventListener('input', function(e) {
    const query = e.target.value.toLowerCase().trim();
    const container = document.querySelector('.biz-partners-list');

    flipFilter(container, '.biz-partner-card', card => {
      const name = card.querySelector('.biz-partner-name').textContent.toLowerCase();
      const desc = card.querySelector('.biz-partner-desc').textContent.toLowerCase();
      return name.includes(query) || desc.includes(query);
    });
  });
});
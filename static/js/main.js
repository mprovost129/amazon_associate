// Main JavaScript entry point

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.js-affiliate-click').forEach(function (link) {
    link.addEventListener('click', function () {
      if (typeof gtag !== 'function') {
        return;
      }
      gtag('event', 'affiliate_click', {
        product_name: link.dataset.productName || '',
        product_category: link.dataset.productCategory || '',
        destination: 'amazon'
      });
    });
  });
});

# Invoice Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a single-file HTML invoice page (پیش‌فاکتور) for a full-stack developer to send to clients for a car dealership website project.

**Architecture:** Single `invoice.html` file with embedded CSS (in `<style>`) and JavaScript (in `<script>`). Contains 10 checkbox items with dynamic pricing, RTL Persian layout, Modern Dark theme with teal accent, and a print stylesheet.

**Tech Stack:** HTML5, CSS3 (Flexbox, Grid, Gradients, Animations), Vanilla JavaScript, CSS `@media print`

**Files:**
- Create: `C:\Users\OMID\Code\car\invoice.html`

---

### Task 1: HTML Structure — Header, Banner & Developer Info

**Files:**
- Create: `C:\Users\OMID\Code\car\invoice.html`

- [ ] **Step 1: Write the HTML header section**

Write the opening HTML structure with proper meta tags, RTL direction, Persian language, and the header section:

```html
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>پیش‌فاکتور طراحی سایت</title>
</head>
<body>

  <!-- ===== HEADER ===== -->
  <header class="invoice-header">
    <div class="container">
      <div class="header-top">
        <div class="brand">
          <div class="brand-name">🚀 OMID DEV</div>
          <div class="brand-sub">طراحی و توسعه وبسایت‌های حرفه‌ای</div>
        </div>
        <div class="invoice-number-box">
          <div class="label">شماره فاکتور</div>
          <div class="value">INV-۱۴۰۴-۰۰۱</div>
        </div>
      </div>
      <div class="header-divider"></div>
      <div class="header-bottom">
        <div class="client-info">
          <div class="label">کارفرما</div>
          <div class="value" id="clientName">شرکت نمونه فروش خودرو</div>
          <div class="sub">تهران - خیابان ولیعصر</div>
        </div>
        <div class="date-info">
          <div class="date-row">
            <span class="label">تاریخ:</span>
            <span class="value" id="invoiceDate">۱۵ تیر ۱۴۰۴</span>
          </div>
          <div class="date-row">
            <span class="label">سررسید:</span>
            <span class="value" id="dueDate">۱۵ مرداد ۱۴۰۴</span>
          </div>
        </div>
      </div>
    </div>
  </header>

  <!-- ===== TITLE BANNER ===== -->
  <div class="title-banner">
    <div class="container">
      <div class="banner-icon">📋</div>
      <div class="banner-text">
        <h1>پیش‌فاکتور طراحی و توسعه وبسایت</h1>
        <p>پروژه: سایت معرفی و فروش خودرو</p>
      </div>
    </div>
  </div>
```

- [ ] **Step 2: Verify the HTML structure visually**

Open `invoice.html` in browser after adding basic CSS in Task 2. For now just confirm no syntax errors by running a quick validator:

Run: `grep -c "</header>" C:\Users\OMID\Code\car\invoice.html`
Expected: 1 (one closing header tag)

- [ ] **Step 3: Commit**

```bash
git add invoice.html
git commit -m "feat: add invoice HTML header structure"
```

---

### Task 2: HTML Structure — Items List (10 Services)

**Files:**
- Modify: `C:\Users\OMID\Code\car\invoice.html` (append after header/banner)

- [ ] **Step 1: Write the items list section**

```html
  <!-- ===== ITEMS LIST ===== -->
  <section class="items-section">
    <div class="container">
      <div class="section-header">
        <h2>📦 شرح خدمات</h2>
      </div>
      <div class="items-list" id="itemsList">

        <!-- Item 1: Homepage -->
        <div class="item-card" data-price="8000000" data-id="home">
          <label class="item-checkbox">
            <input type="checkbox" checked>
            <span class="checkmark"></span>
          </label>
          <div class="item-icon">🏠</div>
          <div class="item-content">
            <div class="item-title">صفحه اصلی (Homepage)</div>
            <div class="item-subtitle">طراحی UI/UX و توسعه فرانت‌اند</div>
            <div class="item-tags">
              <span>✨ هدر و Hero Section</span>
              <span>✨ اسلایدر خودروهای ویژه</span>
              <span>✨ بخش معرفی خدمات</span>
              <span>✨ فرم تماس سریع</span>
              <span>✨ فوتر کامل</span>
              <span>📱 طراحی واکنش‌گرا</span>
            </div>
            <div class="item-meta">
              <span>⏱ زمان تحویل: ۵ روز</span>
              <span>🔄 ویرایش: ۲ مرتبه</span>
            </div>
          </div>
          <div class="item-price">
            <div class="price-label">قیمت</div>
            <div class="price-value">۸,۰۰۰,۰۰۰</div>
            <div class="price-currency">تومان</div>
          </div>
        </div>

        <!-- Item 2: Catalog -->
        <div class="item-card" data-price="12000000" data-id="catalog">
          <label class="item-checkbox">
            <input type="checkbox" checked>
            <span class="checkmark"></span>
          </label>
          <div class="item-icon">🚗</div>
          <div class="item-content">
            <div class="item-title">کاتالوگ خودروها</div>
            <div class="item-subtitle">نمایش لیست خودروها با جزئیات کامل</div>
            <div class="item-tags">
              <span>✨ نمایش گرید و لیست</span>
              <span>✨ تصاویر با گالری</span>
              <span>✨ مشخصات فنی</span>
              <span>✨ قیمت و وضعیت موجودی</span>
              <span>✨ صفحه‌بندی (Pagination)</span>
              <span>📱 واکنش‌گرا</span>
            </div>
            <div class="item-meta">
              <span>⏱ زمان تحویل: ۷ روز</span>
              <span>🔄 ویرایش: ۳ مرتبه</span>
            </div>
          </div>
          <div class="item-price">
            <div class="price-label">قیمت</div>
            <div class="price-value">۱۲,۰۰۰,۰۰۰</div>
            <div class="price-currency">تومان</div>
          </div>
        </div>

        <!-- Item 3: Car Detail -->
        <div class="item-card" data-price="10000000" data-id="detail">
          <label class="item-checkbox">
            <input type="checkbox" checked>
            <span class="checkmark"></span>
          </label>
          <div class="item-icon">📋</div>
          <div class="item-content">
            <div class="item-title">صفحه جزئیات خودرو</div>
            <div class="item-subtitle">نمایش کامل اطلاعات یک خودرو</div>
            <div class="item-tags">
              <span>✨ گالری تصاویر بزرگ</span>
              <span>✨ جدول مشخصات فنی</span>
              <span>✨ انتخاب رنگ و آپشن</span>
              <span>✨ قیمت‌گذاری پویا</span>
              <span>✨ خودروهای مشابه</span>
              <span>📱 واکنش‌گرا</span>
            </div>
            <div class="item-meta">
              <span>⏱ زمان تحویل: ۶ روز</span>
              <span>🔄 ویرایش: ۲ مرتبه</span>
            </div>
          </div>
          <div class="item-price">
            <div class="price-label">قیمت</div>
            <div class="price-value">۱۰,۰۰۰,۰۰۰</div>
            <div class="price-currency">تومان</div>
          </div>
        </div>

        <!-- Item 4: Search & Filter -->
        <div class="item-card" data-price="15000000" data-id="search">
          <label class="item-checkbox">
            <input type="checkbox" checked>
            <span class="checkmark"></span>
          </label>
          <div class="item-icon">🔍</div>
          <div class="item-content">
            <div class="item-title">جستجو و فیلتر پیشرفته</div>
            <div class="item-subtitle">سیستم جستجوی هوشمند خودرو</div>
            <div class="item-tags">
              <span>✨ جستجوی پیشرفته</span>
              <span>✨ فیلتر برند و مدل</span>
              <span>✨ فیلتر سال و قیمت</span>
              <span>✨ فیلتر رنگ و وضعیت</span>
              <span>✨ مرتب‌سازی نتایج</span>
              <span>⚡ جستجوی Ajax</span>
            </div>
            <div class="item-meta">
              <span>⏱ زمان تحویل: ۱۰ روز</span>
              <span>🔄 ویرایش: ۳ مرتبه</span>
            </div>
          </div>
          <div class="item-price">
            <div class="price-label">قیمت</div>
            <div class="price-value">۱۵,۰۰۰,۰۰۰</div>
            <div class="price-currency">تومان</div>
          </div>
        </div>

        <!-- Item 5: About Us -->
        <div class="item-card" data-price="6000000" data-id="about">
          <label class="item-checkbox">
            <input type="checkbox" checked>
            <span class="checkmark"></span>
          </label>
          <div class="item-icon">🏢</div>
          <div class="item-content">
            <div class="item-title">درباره ما</div>
            <div class="item-subtitle">معرفی شرکت و تیم</div>
            <div class="item-tags">
              <span>✨ معرفی شرکت</span>
              <span>✨ تیم و همکاران</span>
              <span>✨ تاریخچه و افتخارات</span>
              <span>✨ گالری تصاویر</span>
              <span>📱 واکنش‌گرا</span>
            </div>
            <div class="item-meta">
              <span>⏱ زمان تحویل: ۳ روز</span>
              <span>🔄 ویرایش: ۲ مرتبه</span>
            </div>
          </div>
          <div class="item-price">
            <div class="price-label">قیمت</div>
            <div class="price-value">۶,۰۰۰,۰۰۰</div>
            <div class="price-currency">تومان</div>
          </div>
        </div>

        <!-- Item 6: Contact Us -->
        <div class="item-card" data-price="5000000" data-id="contact">
          <label class="item-checkbox">
            <input type="checkbox" checked>
            <span class="checkmark"></span>
          </label>
          <div class="item-icon">📞</div>
          <div class="item-content">
            <div class="item-title">تماس با ما</div>
            <div class="item-subtitle">صفحه ارتباط با فروشگاه</div>
            <div class="item-tags">
              <span>✨ فرم تماس پیشرفته</span>
              <span>✨ نقشه تعاملی</span>
              <span>✨ اطلاعات شعب</span>
              <span>✨ ساعات کاری</span>
              <span>✨ اتصال به API</span>
              <span>📱 واکنش‌گرا</span>
            </div>
            <div class="item-meta">
              <span>⏱ زمان تحویل: ۳ روز</span>
              <span>🔄 ویرایش: ۲ مرتبه</span>
            </div>
          </div>
          <div class="item-price">
            <div class="price-label">قیمت</div>
            <div class="price-value">۵,۰۰۰,۰۰۰</div>
            <div class="price-currency">تومان</div>
          </div>
        </div>

        <!-- Item 7: Admin Panel -->
        <div class="item-card" data-price="25000000" data-id="admin">
          <label class="item-checkbox">
            <input type="checkbox" checked>
            <span class="checkmark"></span>
          </label>
          <div class="item-icon">⚙️</div>
          <div class="item-content">
            <div class="item-title">پنل مدیریت</div>
            <div class="item-subtitle">داشبورد مدیریت محتوا</div>
            <div class="item-tags">
              <span>✨ مدیریت خودروها</span>
              <span>✨ مدیریت کاربران</span>
              <span>✨ مدیریت سفارشات</span>
              <span>✨ مدیریت محتوا</span>
              <span>✨ گزارشات آماری</span>
              <span>🔒 سطح دسترسی</span>
            </div>
            <div class="item-meta">
              <span>⏱ زمان تحویل: ۱۴ روز</span>
              <span>🔄 ویرایش: ۴ مرتبه</span>
            </div>
          </div>
          <div class="item-price">
            <div class="price-label">قیمت</div>
            <div class="price-value">۲۵,۰۰۰,۰۰۰</div>
            <div class="price-currency">تومان</div>
          </div>
        </div>

        <!-- Item 8: Blog -->
        <div class="item-card" data-price="8000000" data-id="blog">
          <label class="item-checkbox">
            <input type="checkbox" checked>
            <span class="checkmark"></span>
          </label>
          <div class="item-icon">📝</div>
          <div class="item-content">
            <div class="item-title">وبلاگ / مقالات</div>
            <div class="item-subtitle">سیستم مدیریت محتوا</div>
            <div class="item-tags">
              <span>✨ لیست مقالات</span>
              <span>✨ صفحه مقاله</span>
              <span>✨ دسته‌بندی و برچسب</span>
              <span>✨ جستجوی داخلی</span>
              <span>✨ نظرات کاربران</span>
              <span>📱 واکنش‌گرا</span>
            </div>
            <div class="item-meta">
              <span>⏱ زمان تحویل: ۵ روز</span>
              <span>🔄 ویرایش: ۲ مرتبه</span>
            </div>
          </div>
          <div class="item-price">
            <div class="price-label">قیمت</div>
            <div class="price-value">۸,۰۰۰,۰۰۰</div>
            <div class="price-currency">تومان</div>
          </div>
        </div>

        <!-- Item 9: Compare -->
        <div class="item-card" data-price="7000000" data-id="compare">
          <label class="item-checkbox">
            <input type="checkbox" checked>
            <span class="checkmark"></span>
          </label>
          <div class="item-icon">⚖️</div>
          <div class="item-content">
            <div class="item-title">مقایسه خودروها</div>
            <div class="item-subtitle">مقایسه دو یا چند خودرو</div>
            <div class="item-tags">
              <span>✨ انتخاب چند خودرو</span>
              <span>✨ جدول مقایسه</span>
              <span>✨ مشخصات فنی</span>
              <span>✨ تفاوت قیمت</span>
              <span>✨ نمودار مقایسه</span>
              <span>📱 واکنش‌گرا</span>
            </div>
            <div class="item-meta">
              <span>⏱ زمان تحویل: ۵ روز</span>
              <span>🔄 ویرایش: ۲ مرتبه</span>
            </div>
          </div>
          <div class="item-price">
            <div class="price-label">قیمت</div>
            <div class="price-value">۷,۰۰۰,۰۰۰</div>
            <div class="price-currency">تومان</div>
          </div>
        </div>

        <!-- Item 10: Loan Calculator -->
        <div class="item-card" data-price="12000000" data-id="calc">
          <label class="item-checkbox">
            <input type="checkbox" checked>
            <span class="checkmark"></span>
          </label>
          <div class="item-icon">🧮</div>
          <div class="item-content">
            <div class="item-title">محاسبه اقساط / وام</div>
            <div class="item-subtitle">ماشین حساب تسهیلات بانکی</div>
            <div class="item-tags">
              <span>✨ ماشین حساب اقساط</span>
              <span>✨ محاسبه سود وام</span>
              <span>✨ جدول بازپرداخت</span>
              <span>✨ مقایسه بانک‌ها</span>
              <span>✨ خروجی PDF</span>
              <span>📱 واکنش‌گرا</span>
            </div>
            <div class="item-meta">
              <span>⏱ زمان تحویل: ۷ روز</span>
              <span>🔄 ویرایش: ۳ مرتبه</span>
            </div>
          </div>
          <div class="item-price">
            <div class="price-label">قیمت</div>
            <div class="price-value">۱۲,۰۰۰,۰۰۰</div>
            <div class="price-currency">تومان</div>
          </div>
        </div>

      </div>
    </div>
  </section>
```

- [ ] **Step 2: Verify no HTML syntax errors**

Run: `grep -c "</section>" C:\Users\OMID\Code\car\invoice.html`
Expected: at least 1

- [ ] **Step 3: Commit**

```bash
git add invoice.html
git commit -m "feat: add 10 service items to invoice"
```

---

### Task 3: HTML Structure — Price Summary, Payment Terms & Footer

**Files:**
- Modify: `C:\Users\OMID\Code\car\invoice.html` (append after items list)

- [ ] **Step 1: Write the price summary section**

```html
  <!-- ===== PRICE SUMMARY ===== -->
  <section class="summary-section">
    <div class="container">
      <div class="summary-card">
        <div class="summary-header">
          <h2>💰 خلاصه قیمت</h2>
        </div>
        <div class="summary-rows">
          <div class="summary-row">
            <span>تعداد آیتم‌های انتخاب شده</span>
            <span id="selectedCount">۱۰</span>
          </div>
          <div class="summary-row">
            <span>جمع کل</span>
            <span id="totalPrice">۱۰۸,۰۰۰,۰۰۰ تومان</span>
          </div>
          <div class="summary-row discount-row">
            <span>تخفیف ویژه (۵٪)</span>
            <span id="discountAmount">- ۵,۴۰۰,۰۰۰ تومان</span>
          </div>
          <div class="summary-divider"></div>
          <div class="summary-row final-row">
            <span>💰 مبلغ قابل پرداخت</span>
            <span id="finalPrice">۱۰۲,۶۰۰,۰۰۰ تومان</span>
          </div>
        </div>
        <div class="amount-in-words">
          <span class="label">مبلغ به حروف:</span>
          <span id="amountWords">صد و دو میلیون و ششصد هزار تومان</span>
        </div>
      </div>
    </div>
  </section>

  <!-- ===== PAYMENT TERMS ===== -->
  <section class="payment-section">
    <div class="container">
      <h2>💳 شرایط پرداخت</h2>
      <div class="payment-terms">
        <div class="term-card">
          <div class="term-icon">💳</div>
          <div class="term-label">پیش‌پرداخت</div>
          <div class="term-value">۴۰٪</div>
          <div class="term-desc">هنگام عقد قرارداد</div>
        </div>
        <div class="term-arrow">⬅️</div>
        <div class="term-card">
          <div class="term-icon">🏁</div>
          <div class="term-label">پس از تحویل</div>
          <div class="term-value">۳۰٪</div>
          <div class="term-desc">تحویل نسخه اولیه</div>
        </div>
        <div class="term-arrow">⬅️</div>
        <div class="term-card">
          <div class="term-icon">✅</div>
          <div class="term-label">پس از تأیید</div>
          <div class="term-value">۳۰٪</div>
          <div class="term-desc">تأیید نهایی کارفرما</div>
        </div>
      </div>
    </div>
  </section>

  <!-- ===== FOOTER ===== -->
  <footer class="invoice-footer">
    <div class="container">
      <div class="footer-contact">
        <span>📧 omid@example.com</span>
        <span>📞 ۰۹۱۲-XXX-XXXX</span>
        <span>🌐 omid-dev.ir</span>
      </div>
      <div class="footer-actions">
        <button class="btn btn-primary" onclick="window.print()">🖨️ چاپ فاکتور</button>
        <button class="btn btn-secondary" onclick="resetInvoice()">🔄 بازنشانی</button>
      </div>
      <div class="footer-note">
        این پیش‌فاکتور به مدت ۷ روز اعتبار دارد
      </div>
    </div>
  </footer>

  <script>
    // JavaScript will be added in Task 5
  </script>

</body>
</html>
```

- [ ] **Step 2: Verify structure completeness**

Run: `grep -c "</html>" C:\Users\OMID\Code\car\invoice.html`
Expected: 1

- [ ] **Step 3: Commit**

```bash
git add invoice.html
git commit -m "feat: add price summary, payment terms, and footer"
```

---

### Task 4: CSS Styles — Modern Dark Theme

**Files:**
- Modify: `C:\Users\OMID\Code\car\invoice.html` (add `<style>` inside `<head>`)

- [ ] **Step 1: Add CSS reset, variables, and base styles**

Insert after `<title>` in `<head>`:

```html
  <style>
    /* ===== RESET & BASE ===== */
    *, *::before, *::after {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap');

    :root {
      --bg-primary: #0f1923;
      --bg-secondary: #1a2332;
      --bg-card: #1e2a3a;
      --bg-card-hover: #243040;
      --accent-primary: #00d2ff;
      --accent-secondary: #3a7bd5;
      --accent-gradient: linear-gradient(135deg, #00d2ff, #3a7bd5);
      --text-primary: #ffffff;
      --text-secondary: #8899aa;
      --text-muted: #556677;
      --danger: #ff6b6b;
      --success: #51cf66;
      --warning: #fcc419;
      --border-color: rgba(0, 210, 255, 0.1);
      --border-light: rgba(255, 255, 255, 0.05);
      --shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
      --radius: 12px;
      --radius-sm: 8px;
      --radius-lg: 16px;
      --font: 'Vazirmatn', 'Segoe UI', Tahoma, sans-serif;
      --transition: 0.3s ease;
    }

    body {
      font-family: var(--font);
      background: var(--bg-primary);
      color: var(--text-primary);
      line-height: 1.8;
      min-height: 100vh;
      padding: 20px;
    }

    .container {
      max-width: 900px;
      margin: 0 auto;
      padding: 0 20px;
    }
  </style>
```

- [ ] **Step 2: Add header and banner styles**

Add after base styles:

```css
    /* ===== HEADER ===== */
    .invoice-header {
      background: linear-gradient(135deg, #0f2027, #203a43);
      border-radius: var(--radius-lg) var(--radius-lg) 0 0;
      padding: 32px 0;
    }

    .header-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }

    .brand-name {
      font-size: 24px;
      font-weight: 900;
      color: var(--accent-primary);
      letter-spacing: 1px;
    }

    .brand-sub {
      font-size: 13px;
      color: var(--text-secondary);
      margin-top: 4px;
    }

    .invoice-number-box {
      background: rgba(0, 210, 255, 0.1);
      border: 1px solid rgba(0, 210, 255, 0.2);
      border-radius: var(--radius-sm);
      padding: 10px 20px;
      text-align: center;
    }

    .invoice-number-box .label {
      font-size: 11px;
      color: var(--text-secondary);
      text-transform: uppercase;
      letter-spacing: 1px;
    }

    .invoice-number-box .value {
      font-size: 18px;
      font-weight: 700;
      color: var(--accent-primary);
    }

    .header-divider {
      height: 1px;
      background: var(--border-light);
      margin: 20px 0;
    }

    .header-bottom {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .client-info .label {
      font-size: 12px;
      color: var(--text-secondary);
      margin-bottom: 4px;
    }

    .client-info .value {
      font-size: 16px;
      font-weight: 600;
    }

    .client-info .sub {
      font-size: 13px;
      color: var(--text-secondary);
    }

    .date-info {
      text-align: left;
    }

    .date-row {
      margin-bottom: 4px;
    }

    .date-row .label {
      font-size: 12px;
      color: var(--text-secondary);
      margin-left: 8px;
    }

    .date-row .value {
      font-size: 14px;
      font-weight: 500;
    }

    /* ===== TITLE BANNER ===== */
    .title-banner {
      background: var(--accent-gradient);
      padding: 20px 0;
    }

    .title-banner .container {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .banner-icon {
      font-size: 40px;
    }

    .banner-text h1 {
      font-size: 22px;
      font-weight: 800;
      color: white;
    }

    .banner-text p {
      font-size: 14px;
      opacity: 0.9;
      margin-top: 4px;
    }
```

- [ ] **Step 3: Add items list styles**

```css
    /* ===== ITEMS SECTION ===== */
    .items-section {
      background: var(--bg-secondary);
      padding: 24px 0;
    }

    .section-header {
      margin-bottom: 20px;
    }

    .section-header h2 {
      font-size: 18px;
      font-weight: 700;
    }

    .items-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .item-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      padding: 20px;
      display: flex;
      align-items: flex-start;
      gap: 16px;
      transition: all var(--transition);
      position: relative;
      overflow: hidden;
    }

    .item-card:hover {
      background: var(--bg-card-hover);
      border-color: rgba(0, 210, 255, 0.3);
      transform: translateY(-2px);
      box-shadow: var(--shadow);
    }

    .item-card::before {
      content: '';
      position: absolute;
      top: 0;
      right: 0;
      width: 4px;
      height: 100%;
      background: var(--accent-gradient);
      opacity: 0;
      transition: opacity var(--transition);
    }

    .item-card:hover::before {
      opacity: 1;
    }

    .item-card.unchecked {
      opacity: 0.6;
      border-color: var(--border-light);
    }

    .item-card.unchecked::before {
      opacity: 0;
    }

    /* Checkbox */
    .item-checkbox {
      position: relative;
      width: 24px;
      height: 24px;
      flex-shrink: 0;
      margin-top: 2px;
    }

    .item-checkbox input {
      position: absolute;
      opacity: 0;
      cursor: pointer;
      width: 100%;
      height: 100%;
      z-index: 2;
    }

    .checkmark {
      position: absolute;
      top: 0;
      right: 0;
      width: 24px;
      height: 24px;
      background: transparent;
      border: 2px solid var(--text-secondary);
      border-radius: 6px;
      transition: all var(--transition);
    }

    .item-checkbox input:checked ~ .checkmark {
      background: var(--accent-gradient);
      border-color: var(--accent-primary);
    }

    .checkmark::after {
      content: '✓';
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      color: white;
      font-size: 14px;
      font-weight: 700;
      display: none;
    }

    .item-checkbox input:checked ~ .checkmark::after {
      display: block;
    }

    .item-icon {
      font-size: 32px;
      flex-shrink: 0;
      width: 48px;
      text-align: center;
    }

    .item-content {
      flex: 1;
      min-width: 0;
    }

    .item-title {
      font-size: 16px;
      font-weight: 700;
      color: var(--text-primary);
    }

    .item-subtitle {
      font-size: 13px;
      color: var(--accent-primary);
      margin-top: 2px;
    }

    .item-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 10px;
    }

    .item-tags span {
      background: rgba(0, 210, 255, 0.08);
      color: var(--text-secondary);
      padding: 3px 10px;
      border-radius: 20px;
      font-size: 11px;
      white-space: nowrap;
    }

    .item-meta {
      display: flex;
      gap: 20px;
      margin-top: 10px;
      font-size: 12px;
      color: var(--text-muted);
    }

    .item-price {
      text-align: left;
      flex-shrink: 0;
      min-width: 120px;
      padding-right: 16px;
      border-right: 1px solid var(--border-light);
    }

    .price-label {
      font-size: 11px;
      color: var(--text-secondary);
      text-transform: uppercase;
      letter-spacing: 1px;
    }

    .price-value {
      font-size: 20px;
      font-weight: 800;
      color: var(--accent-primary);
      line-height: 1.3;
    }

    .price-currency {
      font-size: 11px;
      color: var(--text-secondary);
    }
```

- [ ] **Step 4: Add summary, payment terms, and footer styles**

```css
    /* ===== SUMMARY SECTION ===== */
    .summary-section {
      background: var(--bg-secondary);
      padding: 0 0 24px 0;
    }

    .summary-card {
      background: linear-gradient(135deg, #0f2027, #1a2a3a);
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      padding: 24px;
    }

    .summary-header h2 {
      font-size: 18px;
      font-weight: 700;
      margin-bottom: 16px;
    }

    .summary-rows {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .summary-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 15px;
      color: var(--text-secondary);
    }

    .summary-row span:last-child {
      font-weight: 600;
      color: var(--text-primary);
    }

    .discount-row span:last-child {
      color: var(--danger);
    }

    .summary-divider {
      height: 2px;
      background: var(--accent-gradient);
      margin: 4px 0;
      border-radius: 2px;
    }

    .final-row {
      font-size: 20px;
    }

    .final-row span:last-child {
      font-size: 24px;
      font-weight: 900;
      color: var(--accent-primary);
    }

    .amount-in-words {
      margin-top: 16px;
      padding: 12px 16px;
      background: rgba(0, 210, 255, 0.05);
      border-radius: var(--radius-sm);
      border: 1px dashed rgba(0, 210, 255, 0.2);
      font-size: 14px;
      color: var(--text-secondary);
    }

    .amount-in-words .label {
      color: var(--accent-primary);
      font-weight: 600;
      margin-left: 8px;
    }

    /* ===== PAYMENT SECTION ===== */
    .payment-section {
      background: var(--bg-secondary);
      padding: 0 0 24px 0;
    }

    .payment-section h2 {
      font-size: 18px;
      font-weight: 700;
      margin-bottom: 16px;
    }

    .payment-terms {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 12px;
    }

    .term-card {
      flex: 1;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      padding: 20px;
      text-align: center;
      transition: all var(--transition);
    }

    .term-card:hover {
      border-color: rgba(0, 210, 255, 0.3);
      transform: translateY(-2px);
    }

    .term-icon {
      font-size: 32px;
      margin-bottom: 8px;
    }

    .term-label {
      font-size: 13px;
      color: var(--text-secondary);
      margin-bottom: 4px;
    }

    .term-value {
      font-size: 28px;
      font-weight: 900;
      color: var(--accent-primary);
    }

    .term-desc {
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 4px;
    }

    .term-arrow {
      font-size: 24px;
      color: var(--text-muted);
      flex-shrink: 0;
    }

    /* ===== FOOTER ===== */
    .invoice-footer {
      background: linear-gradient(135deg, #203a43, #0f2027);
      border-radius: 0 0 var(--radius-lg) var(--radius-lg);
      padding: 24px 0;
      text-align: center;
    }

    .footer-contact {
      display: flex;
      justify-content: center;
      gap: 24px;
      font-size: 14px;
      color: var(--text-secondary);
    }

    .footer-actions {
      margin: 20px 0;
      display: flex;
      justify-content: center;
      gap: 12px;
    }

    .btn {
      padding: 12px 28px;
      border: none;
      border-radius: var(--radius-sm);
      font-family: var(--font);
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      transition: all var(--transition);
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }

    .btn-primary {
      background: var(--accent-gradient);
      color: white;
    }

    .btn-primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 16px rgba(0, 210, 255, 0.3);
    }

    .btn-secondary {
      background: transparent;
      color: var(--text-secondary);
      border: 1px solid var(--border-color);
    }

    .btn-secondary:hover {
      background: var(--bg-card);
      color: var(--text-primary);
    }

    .footer-note {
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 12px;
    }
```

- [ ] **Step 5: Add responsive and print styles**

```css
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
      body { padding: 10px; }
      .container { padding: 0 12px; }
      .header-top { flex-direction: column; gap: 16px; }
      .header-bottom { flex-direction: column; gap: 12px; text-align: center; }
      .date-info { text-align: center; }
      .item-card { flex-wrap: wrap; }
      .item-price {
        width: 100%;
        text-align: center;
        border-right: none;
        border-top: 1px solid var(--border-light);
        padding-right: 0;
        padding-top: 12px;
      }
      .payment-terms { flex-direction: column; }
      .term-arrow { transform: rotate(90deg); }
      .footer-contact { flex-direction: column; gap: 8px; }
      .footer-actions { flex-direction: column; align-items: center; }
      .banner-text h1 { font-size: 18px; }
      .price-value { font-size: 18px; }
    }

    @media (max-width: 480px) {
      .invoice-header { padding: 20px 0; }
      .item-tags span { font-size: 10px; }
      .item-card { padding: 14px; }
    }

    /* ===== PRINT STYLES ===== */
    @media print {
      body {
        background: white !important;
        padding: 0 !important;
        color: #333 !important;
      }
      .invoice-header {
        background: #f8f9fa !important;
        border-bottom: 3px solid #00d2ff !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }
      .brand-name { color: #1a73e8 !important; }
      .invoice-number-box { border-color: #ddd !important; }
      .invoice-number-box .value { color: #1a73e8 !important; }
      .title-banner {
        background: #1a73e8 !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }
      .items-section { background: white !important; }
      .item-card {
        background: #f8f9fa !important;
        border-color: #ddd !important;
        break-inside: avoid;
        page-break-inside: avoid;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }
      .item-card:hover { transform: none !important; box-shadow: none !important; }
      .item-card::before { display: none !important; }
      .item-title { color: #333 !important; }
      .item-subtitle { color: #1a73e8 !important; }
      .item-tags span { background: #e8f0fe !important; color: #555 !important; }
      .price-value { color: #1a73e8 !important; }
      .summary-section { background: white !important; }
      .summary-card { background: #f8f9fa !important; border-color: #ddd !important; }
      .summary-row { color: #555 !important; }
      .summary-row span:last-child { color: #333 !important; }
      .final-row span:last-child { color: #1a73e8 !important; }
      .amount-in-words { border-color: #ddd !important; }
      .payment-section { background: white !important; }
      .term-card { background: #f8f9fa !important; border-color: #ddd !important; }
      .term-value { color: #1a73e8 !important; }
      .invoice-footer { background: #f8f9fa !important; border-top: 2px solid #ddd !important; }
      .footer-contact { color: #555 !important; }
      .footer-actions { display: none !important; }
      .footer-note { color: #999 !important; }
      .item-checkbox input:checked ~ .checkmark { background: #1a73e8 !important; }
      .item-card.unchecked { opacity: 0.4 !important; }
      .summary-divider { background: #1a73e8 !important; }
    }

    /* ===== ANIMATIONS ===== */
    @keyframes fadeInUp {
      from {
        opacity: 0;
        transform: translateY(20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    .item-card {
      animation: fadeInUp 0.4s ease forwards;
    }

    .item-card:nth-child(1) { animation-delay: 0.05s; }
    .item-card:nth-child(2) { animation-delay: 0.10s; }
    .item-card:nth-child(3) { animation-delay: 0.15s; }
    .item-card:nth-child(4) { animation-delay: 0.20s; }
    .item-card:nth-child(5) { animation-delay: 0.25s; }
    .item-card:nth-child(6) { animation-delay: 0.30s; }
    .item-card:nth-child(7) { animation-delay: 0.35s; }
    .item-card:nth-child(8) { animation-delay: 0.40s; }
    .item-card:nth-child(9) { animation-delay: 0.45s; }
    .item-card:nth-child(10) { animation-delay: 0.50s; }

    /* ===== COUNTER BADGE ===== */
    .count-badge {
      display: inline-block;
      background: var(--accent-gradient);
      color: white;
      padding: 2px 12px;
      border-radius: 20px;
      font-size: 14px;
      font-weight: 600;
      margin-right: 8px;
    }
  </style>
```

- [ ] **Step 6: Verify CSS is properly closed**

Run: `grep "</style>" C:\Users\OMID\Code\car\invoice.html`
Expected: 1

- [ ] **Step 7: Commit**

```bash
git add invoice.html
git commit -m "feat: add Modern Dark theme CSS with print and responsive styles"
```

---

### Task 5: JavaScript — Dynamic Pricing, Checkbox Logic & Number Formatting

**Files:**
- Modify: `C:\Users\OMID\Code\car\invoice.html` (replace empty `<script>` block)

- [ ] **Step 1: Write the JavaScript for dynamic pricing**

Replace the empty `<script>` block at the end of the body:

```html
  <script>
    // ===== Number Formatting =====
    function formatNumber(num) {
      return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }

    // ===== Update Invoice Totals =====
    function updateInvoice() {
      const items = document.querySelectorAll('.item-card');
      let total = 0;
      let count = 0;

      items.forEach(item => {
        const checkbox = item.querySelector('input[type="checkbox"]');
        const price = parseInt(item.dataset.price);

        if (checkbox.checked) {
          total += price;
          count++;
          item.classList.remove('unchecked');
        } else {
          item.classList.add('unchecked');
        }
      });

      const discount = Math.round(total * 0.05);
      const finalTotal = total - discount;

      document.getElementById('selectedCount').textContent = count;
      document.getElementById('totalPrice').textContent = formatNumber(total) + ' تومان';
      document.getElementById('discountAmount').textContent = '- ' + formatNumber(discount) + ' تومان';
      document.getElementById('finalPrice').textContent = formatNumber(finalTotal) + ' تومان';
      document.getElementById('amountWords').textContent = numberToWords(finalTotal);
    }

    // ===== Number to Persian Words =====
    function numberToWords(num) {
      if (num === 0) return 'صفر تومان';

      const ones = ['', 'یک', 'دو', 'سه', 'چهار', 'پنج', 'شش', 'هفت', 'هشت', 'نه'];
      const tens = ['', 'ده', 'بیست', 'سی', 'چهل', 'پنجاه', 'شصت', 'هفتاد', 'هشتاد', 'نود'];
      const hundreds = ['', 'صد', 'دویست', 'سیصد', 'چهارصد', 'پانصد', 'ششصد', 'هفتصد', 'هشتصد', 'نهصد'];
      const thousands = ['', 'هزار', 'میلیون', 'میلیارد', 'تریلیون'];

      if (num < 10) return ones[num] + ' تومان';
      if (num < 100) {
        if (num % 10 === 0) return tens[Math.floor(num / 10)] + ' تومان';
        return tens[Math.floor(num / 10)] + ' و ' + ones[num % 10] + ' تومان';
      }

      // For large numbers, use a simpler approach
      if (num >= 1000000) {
        const mil = Math.floor(num / 1000000);
        const rem = num % 1000000;
        let result = '';
        if (mil === 1) result = 'یک میلیون';
        else if (mil === 2) result = 'دو میلیون';
        else result = formatNumber(mil) + ' میلیون';
        if (rem > 0) {
          result += ' و ' + numberToWordsSimple(rem);
        }
        return result + ' تومان';
      }

      return numberToWordsSimple(num) + ' تومان';
    }

    function numberToWordsSimple(num) {
      if (num === 0) return '';
      if (num < 10) return ['', 'یک', 'دو', 'سه', 'چهار', 'پنج', 'شش', 'هفت', 'هشت', 'نه'][num];
      if (num < 100) {
        const tens = ['', 'ده', 'بیست', 'سی', 'چهل', 'پنجاه', 'شصت', 'هفتاد', 'هشتاد', 'نود'];
        const ones = ['', 'یک', 'دو', 'سه', 'چهار', 'پنج', 'شش', 'هفت', 'هشت', 'نه'];
        if (num % 10 === 0) return tens[Math.floor(num / 10)];
        return tens[Math.floor(num / 10)] + ' و ' + ones[num % 10];
      }
      if (num < 1000) {
        const hundreds = ['', 'صد', 'دویست', 'سیصد', 'چهارصد', 'پانصد', 'ششصد', 'هفتصد', 'هشتصد', 'نهصد'];
        const rem = num % 100;
        if (rem === 0) return hundreds[Math.floor(num / 100)];
        return hundreds[Math.floor(num / 100)] + ' و ' + numberToWordsSimple(rem);
      }
      if (num < 1000000) {
        const thou = Math.floor(num / 1000);
        const rem = num % 1000;
        let result = '';
        if (thou === 1) result = 'یک هزار';
        else result = numberToWordsSimple(thou) + ' هزار';
        if (rem > 0) result += ' و ' + numberToWordsSimple(rem);
        return result;
      }
      return formatNumber(num);
    }

    // ===== Reset Invoice =====
    function resetInvoice() {
      const items = document.querySelectorAll('.item-card input[type="checkbox"]');
      items.forEach(cb => cb.checked = true);
      updateInvoice();
    }

    // ===== Init =====
    document.addEventListener('DOMContentLoaded', function() {
      const checkboxes = document.querySelectorAll('.item-card input[type="checkbox"]');
      checkboxes.forEach(cb => {
        cb.addEventListener('change', updateInvoice);
      });
      updateInvoice();
    });
  </script>
```

- [ ] **Step 2: Verify script loads without errors**

Open `invoice.html` in browser and check browser console for errors. Verify:
- All 10 items show and are checked
- Unchecking items updates the total
- Reset button restores all items

Run: `grep -c "</script>" C:\Users\OMID\Code\car\invoice.html`
Expected: at least 1

- [ ] **Step 3: Commit**

```bash
git add invoice.html
git commit -m "feat: add dynamic pricing and number-to-words JavaScript"
```

---

### Task 6: Final Integration & Print Test

**Files:**
- Modify: `C:\Users\OMID\Code\car\invoice.html`

- [ ] **Step 1: Verify full file integrity**

Open the file in browser and confirm:
1. ✅ Header displays correctly with brand name and invoice number
2. ✅ Banner shows project title
3. ✅ All 10 item cards render with icons, tags, and prices
4. ✅ Checkboxes work — unchecking an item grays it out and updates total
5. ✅ Price summary shows count, total, discount, and final total
6. ✅ Amount in words displays correctly
7. ✅ Payment terms cards are visible
8. ✅ Footer has contact info, print button, and reset button
9. ✅ Print button triggers browser print dialog
10. ✅ Print preview shows clean white layout without action buttons

- [ ] **Step 2: Test mobile responsiveness**

Open browser dev tools and test at 375px width. Verify:
- Items stack vertically
- Price moves below content
- Payment terms stack vertically
- Footer buttons stack

- [ ] **Step 3: Final commit**

```bash
git add invoice.html
git commit -m "feat: complete invoice page with full styling and dynamic pricing"
```

document.addEventListener('DOMContentLoaded', () => {
    // Dark Mode Toggle Logic
    const themeToggle = document.querySelector('.theme-toggle');
    const body = document.body;
    const icon = themeToggle ? themeToggle.querySelector('i') : null;

    // Check saved preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark-mode');
        if (icon) icon.className = 'fas fa-sun';
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            body.classList.toggle('dark-mode');
            const isDark = body.classList.contains('dark-mode');
            
            // Update icon
            if (icon) {
                icon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
            }
            
            // Save preference
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        });
    }

    // Mobile Navigation Toggle
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            hamburger.classList.toggle('active');
            
            const spans = hamburger.querySelectorAll('span');
            if (navLinks.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 6px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(5px, -6px)';
                document.body.style.overflow = 'hidden';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
                document.body.style.overflow = '';
            }
        });
    }

    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            if (navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                hamburger.classList.remove('active');
                const spans = hamburger.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
                document.body.style.overflow = '';
            }
        });
    });

    // Publication Search & Highlighting
    const searchInput = document.getElementById('pubSearch');
    const pubCards = document.querySelectorAll('.publication-card');
    const originalContent = new Map();

    if (pubCards.length > 0) {
        pubCards.forEach((card, index) => {
            originalContent.set(index, card.innerHTML);
        });
    }

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.trim().toLowerCase();
            
            pubCards.forEach((card, index) => {
                const title = card.querySelector('h3').textContent;
                const authors = card.querySelector('.authors') ? card.querySelector('.authors').textContent : '';
                const abstract = card.querySelector('.abstract') ? card.querySelector('.abstract').textContent : '';
                const text = title + ' ' + authors + ' ' + abstract;
                
                // Reset content
                card.innerHTML = originalContent.get(index);
                
                if (searchTerm === '') {
                    card.style.display = 'flex';
                    return;
                }

                if (text.toLowerCase().includes(searchTerm)) {
                    card.style.display = 'flex';
                    highlightText(card, searchTerm);
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    function highlightText(element, term) {
        if (!term) return;
        const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT, null, false);
        const textNodes = [];
        while (walker.nextNode()) {
            textNodes.push(walker.currentNode);
        }

        textNodes.forEach(node => {
            const parent = node.parentNode;
            if (parent.tagName === 'SCRIPT' || parent.tagName === 'STYLE' || parent.tagName === 'MARK') return;

            const text = node.textContent;
            if (text.toLowerCase().includes(term)) {
                const regex = new RegExp(`(${escapeRegExp(term)})`, 'gi');
                const newHtml = text.replace(regex, '<mark>$1</mark>');
                const span = document.createElement('span');
                span.innerHTML = newHtml;
                parent.replaceChild(span, node);
                parent.innerHTML = parent.innerHTML.replace(/<span>(.*?)<\/span>/g, '$1'); 
            }
        });
    }

    function escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    // Scroll Animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.card, h2, .education-item').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        observer.observe(el);
    });
    
    const addVisible = () => {
        document.querySelectorAll('.visible').forEach(el => {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        });
    };
    
    setInterval(addVisible, 100);
});

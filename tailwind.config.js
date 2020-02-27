module.exports = {
    theme: {
        extend: {
            colors: {
                primary: {
                    '50': '#ffe7e6',
                    '100': '#ffc7b8',
                    '200': '#ffa28a',
                    '300': '#ff795b',
                    '400': '#ff5436',
                    '500': '#ff200c'
                },
                secondary: {
                    '50': '#d7fcfb',
                    '100': '#97f7f5',
                    '200': '#00f2f2',
                    '300': '#00e9ee',
                    '400': '#00e1e9',
                    '500': '#00d9e9',
                    '600': '#00c8d5',
                    '700': '#00b2b9',
                    '800': '#009da0',
                    '900': '#007870'
                },
                // basic: {
                //   "200": "#e9eeee",
                //   "300": "#dbdfdf",
                //   "400": "#b8bcbc",
                //   "500": "#999d9d",
                //   "600": "#707474",
                //   "700": "#5c6060"
                // },
                dt: {
                    '0': '#121212',
                    '1': '#1e1e1e',
                    '2': '#232323',
                    '3': '#252525',
                    '4': '#282828',
                    '5': '#2c2c2c',
                    '6': '#2F2F2F',
                    '7': '#343434',
                    '8': '#363636',
                    '9': '#383838'
                }
            },
            textColor: {
                error: 'var(--color-error-text)',
                primary: 'var(--color-text)',
                tag: 'var(--color-tag)',
                'tag-hover': 'var(--color-tag-hover)',
                'tag-item-hover': 'var(--color-tag-item-hover)'
            },
            opacity: {
                'high-emphasis': 'var(--opacity-text-high-emphasis)',
                'medium-emphasis': 'var(--opacity-text-medium-emphasis)',
                disabled: 'var(--opacity-text-disabled)'
            },
            backgroundColor: {
                main: 'var(--color-bg-main)',
                'surface-1': 'var(--color-bg-surface-1)',
                'surface-2': 'var(--color-bg-surface-2)',
                tag: 'var(--color-bg-tag)',
                'tag-hover': 'var(--color-bg-tag-hover)',
                basic: 'var(--color-bg-basic)',
                'basic-hover': 'var(--color-bg-basic-hover)',
                'button-disabled': 'var(--color-bg-button-disabled)',
                primary: 'var(--color-bg-primary)',
                'primary-hover': 'var(--color-bg-primary-hover)',
                'nav-link-hover': 'var(--color-bg-nav-link-hover)',
                alternate: 'var(--color-bg-alternate)',
                success: 'var(--color-bg-success)'
            },
            borderColor: {
                default: 'var(--color-border-default)',
                'input-selected': 'var(--color-border-input-selected)',
                error: 'var(--color-border-error)',
                basic: 'var(--color-bg-basic)'
            },
            borderWidth: {
                'image-card': 'var(--width-border-image-card)'
            },
            minHeight: {
                'double-screen': '200vh'
            },
            minWidth: {
                '64': '16rem'
            },
            padding: {
                'nav-perf': '1.3rem'
            },
            width: {
                '77': '19.25rem',
                '96': '24rem'
            }
        }
    },
    variants: {},
    plugins: []
};

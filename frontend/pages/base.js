/**
 * 
 * @param {string} title 
 * @param {string} content 
 * @param {?Object} preloadedState
 * 
 * @returns {string} 
 */
const Page = (title, content, preloadedState) => `
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="initial-scale=1.0">
                <meta http-equiv="X-UA-Compatible" content="ie=edge">
                <title>${title}</title>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/antd/3.26.12/antd.css">
            </head>
            <body>
                ${content}
            
                ${typeof preloadedState !== 'undefined' ? `
                    <script>
                        window.__PRELOADED_STATE__ = ${JSON.stringify(preloadedState)};
                    </script>
                ` : ''}
            
                <script src="/static/js/app.js"></script>
            </body>
        </html>
    `;

export default Page;
const config = {
  title: 'Meme Arcade',
  tagline: 'Quick games. Big meme energy.',
  url: 'https://hassanvfx.github.io',
  baseUrl: '/meme-arcade-book/',
  organizationName: 'hassanvfx',
  projectName: 'meme-arcade-book',
  onBrokenLinks: 'throw',
  presets: [['classic', {docs: false, blog: false}]],
  themeConfig: {navbar: {title: 'Meme Arcade', style: 'dark', items: [{to: '/', label: 'Play', position: 'left'}, {to: '/activities/', label: 'Source activities', position: 'left'}, {to: '/support/', label: 'Support', position: 'left'}]}, footer: {style: 'dark', links: [], copyright: `Copyright © ${new Date().getFullYear()} Hassan Uriostegui · Waken AI Labs.`}}
};
export default config;

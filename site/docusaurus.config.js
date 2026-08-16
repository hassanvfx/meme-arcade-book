const config = {
  title: 'Modern iOS Architecture',
  tagline: 'Deconstructing the $3B MemeArcade',
  url: 'https://hassanvfx.github.io',
  baseUrl: '/meme-arcade-book/',
  organizationName: 'hassanvfx',
  projectName: 'meme-arcade-book',
  onBrokenLinks: 'throw',
  presets: [['classic', {docs: false, blog: false}]],
  themeConfig: {navbar: {title: 'Modern iOS Architecture', items: [{to: '/', label: 'Start here', position: 'left'}, {to: '/activities/', label: 'Source activities', position: 'left'}, {href: 'https://github.com/hassanvfx/meme-arcade-book', label: 'Publishing repository', position: 'right'}]}, footer: {style: 'dark', links: [], copyright: `Copyright © ${new Date().getFullYear()} Hassan Uriostegui · Waken AI Labs. Book content is all rights reserved.`}}
};
export default config;

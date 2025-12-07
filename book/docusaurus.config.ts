import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'AI-Driven Book',
  tagline: 'Built with Spec-Kit Plus and Claude Code',
  favicon: 'img/favicon.ico',

  // Docusaurus future flags
  future: {
    v4: true,
  },

  // Vercel deployment settings
  url: 'https://chatbot-hackatone.vercel.app', // your Vercel URL
  baseUrl: '/', // root path for Vercel

  // GitHub config for edit links (optional)
  organizationName: 'hn8378429', // your GitHub username
  projectName: 'chatbot-hackatone',

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/', // serve docs at site root
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/hn8378429/chatbot-hackatone/tree/main/book/',
        },
        blog: false, // no blog
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'AI-Driven Book',
      logo: {
        alt: 'Book Logo',
        src: 'img/book-logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'bookSidebar',
          position: 'left',
          label: '📚 Read Book',
        },
        {
          to: '/login',
          label: 'Login',
          position: 'right',
        },
        {
          to: '/signup',
          label: 'Sign Up',
          position: 'right',
          className: 'navbar-signup-button',
        },
        {
          href: 'https://github.com/hn8378429/chatbot-hackatone',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Book',
          items: [
            { label: 'Start Reading', to: '/intro' },
          ],
        },
        {
          title: 'Features',
          items: [
            { label: 'AI Chatbot', to: '/intro' },
            { label: 'Translation', to: '/intro' },
            { label: 'Personalization', to: '/intro' },
          ],
        },
        {
          title: 'More',
          items: [
            { label: 'GitHub', href: 'https://github.com/hn8378429/chatbot-hackatone' },
            { label: 'Get Gemini API Key', href: 'https://aistudio.google.com/apikey' },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} AI-Driven Book Project. Built with Docusaurus, FastAPI & Gemini AI.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;

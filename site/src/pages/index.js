import React from 'react';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './index.module.css';

const APP_STORE_URL = 'https://apps.apple.com/us/app/meme-arcade/id6801929719';
const BOOK_URL = 'https://www.lulu.com/shop/hassan-uriostegui/ai-from-tensors-to-agents-on-mac-silicon/hardcover/product-e7qy7gy.html';

const screens = [
  {
    file: 'screenshot-01.png',
    alt: 'Meme Arcade game screen showing a fast arcade driving game with brake and gas controls.',
    label: 'Play instantly',
  },
  {
    file: 'screenshot-02.png',
    alt: 'Meme Arcade discovery screen with a feed of community-made games and categories.',
    label: 'Discover new favorites',
  },
  {
    file: 'screenshot-03.png',
    alt: 'Meme Arcade profile screen with play history, favorites, and game cards.',
    label: 'Track your hype',
  },
];

export default function Home() {
  const appIcon = useBaseUrl('/img/memearcade-app-icon.png');
  const caseStudyAssetPath = useBaseUrl('/img/case-study/');

  return (
    <main className={styles.page}>
      <section className={styles.hero} aria-labelledby="hero-title">
        <div className={styles.heroCopy}>
          <p className={styles.eyebrow}>Meme Arcade for iPhone</p>
          <h1 id="hero-title">Your next favorite game is one scroll away.</h1>
          <p className={styles.lede}>
            Discover bite-size games, jump straight into the action, and build your personal arcade.
          </p>
          <div className={styles.actions}>
            <a className={styles.primaryAction} href={APP_STORE_URL}>
              Download on the App Store <span aria-hidden="true">→</span>
            </a>
            <a className={styles.secondaryAction} href={BOOK_URL}>
              Case Study Book <span aria-hidden="true">↗</span>
            </a>
          </div>
          <p className={styles.availability}>Available on iPhone</p>
        </div>

        <div className={styles.heroArt} aria-hidden="true">
          <img className={styles.heroImage} src={appIcon} alt="" width="1254" height="1254" />
        </div>
      </section>

      <section className={styles.experience} aria-labelledby="experience-title">
        <div className={styles.sectionHeading}>
          <p className={styles.eyebrow}>One arcade, made for your feed</p>
          <h2 id="experience-title">Play, discover, repeat.</h2>
          <p>
            Meme Arcade brings quick games and the culture around them into one lively, scrollable place.
          </p>
        </div>
        <div className={styles.gallery}>
          {screens.map((screen) => (
            <figure className={styles.screenCard} key={screen.file}>
              <img src={`${caseStudyAssetPath}${screen.file}`} alt={screen.alt} loading="lazy" width="1242" height="2688" />
              <figcaption>{screen.label}</figcaption>
            </figure>
          ))}
        </div>
      </section>

      <section className={styles.bookCallout} aria-labelledby="book-title">
        <p className={styles.eyebrow}>Behind the arcade</p>
        <h2 id="book-title">Explore the Meme Arcade case study.</h2>
        <p>
          See the iOS architecture and product thinking behind the experience in <em>AI: From Tensors to Agents on Mac Silicon</em>.
        </p>
        <a className={styles.bookLink} href={BOOK_URL}>Case Study Book <span aria-hidden="true">↗</span></a>
      </section>

      <footer className={styles.footer}>
        <Link to="/activities/">Source activities</Link>
        <Link to="/support/">Support</Link>
        <Link to="/privacy/">Privacy</Link>
        <Link to="/terms/">Terms</Link>
      </footer>
    </main>
  );
}

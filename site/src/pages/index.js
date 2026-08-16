import React from 'react';
import styles from './index.module.css';

const APP_STORE_URL = 'https://apps.apple.com/us/app/meme-arcade/id6801929719';

export default function Home() {
  return (
    <main className={styles.page}>
      <p className={styles.eyebrow}>Waken AI Labs</p>
      <h1>Modern iOS Architecture</h1>
      <p className={styles.subtitle}>Deconstructing the $3B MemeArcade</p>
      <p className={styles.byline}>By Hassan Uriostegui · Waken AI Labs</p>
      <p className={styles.intro}>
        This site is a reader bridge to the original public repositories and articles behind the book. It does not reproduce the course; use the source activities to study the original work directly.
      </p>

      <section className={styles.appCard} aria-labelledby="app-title">
        <img
          className={styles.appIcon}
          src="/meme-arcade-book/img/memearcade-app-icon.png"
          alt="MemeArcade app icon: neon arcade cabinet with game controls."
          width="156"
          height="156"
        />
        <div>
          <p className={styles.kicker}>MemeArcade, the App</p>
          <h2 id="app-title">Explore the iOS case study</h2>
          <p>
            MemeArcade, the App, is the iOS product studied throughout this book: a native shell that orchestrates state, remote gameplay, and device-bound experiences.
          </p>
          <a className={styles.download} href={APP_STORE_URL}>
            Download on the App Store <span aria-hidden="true">→</span>
          </a>
          <p className={styles.note}>
            The $3B framing refers to the broader AI-gaming market, not to the app’s valuation or financing.
          </p>
        </div>
      </section>
    </main>
  );
}

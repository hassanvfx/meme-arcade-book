import React from 'react';
import Link from '@docusaurus/Link';
import styles from './legal.module.css';

export default function Terms() {
  return (
    <main className={styles.page}>
      <p className={styles.eyebrow}>Waken AI · Last updated August 15, 2026</p>
      <h1>Meme Arcade Terms of Use</h1>
      <p className={styles.intro}>This open-source app is provided for entertainment and evaluation.</p>

      <section className={styles.section}>
        <h2>Local app</h2>
        <p>Meme Arcade does not create an account, sell subscriptions, or provide purchases. Favorites, play history, and onboarding state stay on your device.</p>
      </section>

      <section className={styles.section}>
        <h2>Game content</h2>
        <p>Some catalog games and artwork are served by public static hosts. Their availability and content are outside the app’s control.</p>
      </section>

      <section className={styles.section}>
        <h2>Acceptable use</h2>
        <p>Do not use the app to violate law, infringe rights, or interfere with public game hosts.</p>
      </section>

      <section className={styles.section}>
        <h2>Disclaimer</h2>
        <p>The app is provided “as is,” without warranties. Use it at your own risk.</p>
      </section>

      <section className={styles.section}>
        <h2>Contact</h2>
        <p>Questions: <a href="mailto:hello@waken.ai">hello@waken.ai</a>.</p>
      </section>

      <Link className={styles.back} to="/support/">← Meme Arcade Support</Link>
    </main>
  );
}

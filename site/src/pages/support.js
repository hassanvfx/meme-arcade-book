import React from 'react';
import Link from '@docusaurus/Link';
import styles from './legal.module.css';

export default function Support() {
  return (
    <main className={styles.page}>
      <p className={styles.eyebrow}>Waken AI</p>
      <h1>Meme Arcade Support</h1>
      <p className={styles.intro}>
        Meme Arcade is a local-first iOS app for discovering and playing bite-size web games. For help,
        feedback, or a content report, email <a href="mailto:hello@waken.ai">hello@waken.ai</a>.
      </p>

      <section className={styles.section}>
        <h2>Report a game or other content</h2>
        <p>
          Include the game title or link, a short description of the issue, and any context that will help
          us review the report. You can copy a game link from the game player before writing your email.
        </p>
      </section>

      <section className={styles.section}>
        <h2>Your local activity</h2>
        <p>
          Favorites, play history, and onboarding progress are stored on your device. Removing the app may
          remove this local activity.
        </p>
      </section>

      <section className={styles.section}>
        <h2>Policies</h2>
        <ul className={styles.links}>
          <li><Link to="/privacy/">Privacy Notice</Link></li>
          <li><Link to="/terms/">Terms of Use</Link></li>
        </ul>
      </section>

      <Link className={styles.back} to="/">← Back to Meme Arcade</Link>
    </main>
  );
}

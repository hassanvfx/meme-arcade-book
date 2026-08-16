import React from 'react';
import Link from '@docusaurus/Link';
import styles from './legal.module.css';

export default function Privacy() {
  return (
    <main className={styles.page}>
      <p className={styles.eyebrow}>Waken AI · Last updated August 15, 2026</p>
      <h1>Meme Arcade Privacy Notice</h1>
      <p className={styles.intro}>Meme Arcade is designed as a local-first app.</p>

      <section className={styles.section}>
        <h2>Data stored on your device</h2>
        <p>Meme Arcade stores favorites, play history, and onboarding progress locally so it can remember your activity.</p>
      </section>

      <section className={styles.section}>
        <h2>No configured tracking SDKs</h2>
        <p>This build does not initialize account, payment, push, analytics, attribution, or crash-reporting vendors.</p>
      </section>

      <section className={styles.section}>
        <h2>Static game hosts</h2>
        <p>Opening a catalog game can contact its public static host. Those hosts may process network information under their own policies.</p>
      </section>

      <section className={styles.section}>
        <h2>Email reports</h2>
        <p>If you email a report, the message and any details you choose to include are handled by your email provider and the recipient.</p>
      </section>

      <section className={styles.section}>
        <h2>Contact</h2>
        <p>Questions: <a href="mailto:hello@waken.ai">hello@waken.ai</a>.</p>
      </section>

      <Link className={styles.back} to="/support/">← Meme Arcade Support</Link>
    </main>
  );
}

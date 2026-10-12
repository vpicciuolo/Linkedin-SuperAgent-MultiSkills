# Analytics import guide

The local analyzer accepts CSV headers case-insensitively and recognizes common
aliases:

- impressions: `impressions`, `views`, `post impressions`;
- reactions: `reactions`, `likes`;
- comments: `comments`;
- reposts: `reposts`, `shares`;
- saves: `saves`, `bookmarks`;
- sends: `sends`, `shares in messages`;
- followers: `followers`, or pass `--followers`;
- title: `title`, `post`, `post title`, `hook`, `content`;
- published date: `published_at`, `date`, `created at`.

Numbers may contain commas, percent signs, or blanks. Blanks remain unknown.
Rows with zero or missing impressions cannot produce normalized rates and must
be listed separately.

Do not infer revenue or leads from engagement. Ask the user for their goal and
connect performance to that goal when the necessary fields exist.

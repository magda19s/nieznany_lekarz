export const stringToColor = (string: string) => {
  let hash = 0;
  for (let i = 0; i < string.length; i++) {
    hash = string.charCodeAt(i) + ((hash << 5) - hash);
  }

  const pastelize = (base: number, bias: number) =>
    Math.round((base % 128) + 127 + bias);

  const r = pastelize((hash >> 0) & 0xff, -30);
  const g = pastelize((hash >> 8) & 0xff, 10);
  const b = pastelize((hash >> 16) & 0xff, 20);

  const color = `#${[r, g, b]
    .map((x) => x.toString(16).padStart(2, '0'))
    .join('')}`;

  return color;
};

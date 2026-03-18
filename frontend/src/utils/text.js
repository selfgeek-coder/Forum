export function capitalizeFirstLetter(input) {
  if (typeof input !== "string") return "";

  // keep leading whitespace while capitalizing first non-space char
  const match = input.match(/^(\s*)(\S)([\s\S]*)$/);
  if (!match) return input;

  const [, leading, first, rest] = match;
  return leading + first.toUpperCase() + rest;
}


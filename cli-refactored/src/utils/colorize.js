const ANSI_COLORS = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
};

export const colorize = {
  red: (text) => `${ANSI_COLORS.red}${text}${ANSI_COLORS.reset}`,
  green: (text) => `${ANSI_COLORS.green}${text}${ANSI_COLORS.reset}`,
  yellow: (text) => `${ANSI_COLORS.yellow}${text}${ANSI_COLORS.reset}`,
  bold: (text) => `${ANSI_COLORS.bold}${text}${ANSI_COLORS.reset}`,
  dim: (text) => `${ANSI_COLORS.dim}${text}${ANSI_COLORS.reset}`,
};

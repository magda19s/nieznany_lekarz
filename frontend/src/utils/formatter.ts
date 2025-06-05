export const locale = "pl-PL";

export const formatDayMonth = (date: Date): string => {
  const formatter = Intl.DateTimeFormat(locale, {
    month: "2-digit",
    day: "2-digit",
  });

  return formatter.format(date);
};

export const formatTime = (date: Date): string => {
  const formatter = Intl.DateTimeFormat(locale, {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });

  return formatter.format(date);
};

export const formatDate = (date: Date, join = ".", reverse = false): string => {
  const formatter = Intl.DateTimeFormat(locale, {
    month: "2-digit",
    day: "2-digit",
    year: "numeric",
  });

  const [day, month, year] = formatter.format(date).split(".");
  return reverse ? `${year}${join}${month}${join}${day}` : `${day}${join}${month}${join}${year}`;
};

export const formatDateTime = (date: Date, join = ".", reverse = false): string => {
  return `${formatDate(date, join, reverse)} ${formatTime(date)}`;
};

export const formatWeekDayName = (date: Date): string => {
  const formatter = Intl.DateTimeFormat(locale, {
    weekday: "short",
  });
  const weekDayName = formatter.format(date);
  const formattedWeekDayName = weekDayName.charAt(0).toUpperCase() + weekDayName.slice(1);

  return formattedWeekDayName;
};

export const formatAddress = (address: string): string => {
  return address.replace(" | ", ", ");
};

export const formatServiceName = (name: string): string => {
  return name.split("|")[0];
};

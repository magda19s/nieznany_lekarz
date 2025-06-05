import { User as UserIcon } from "lucide-react";
import { Avatar as UiAvatar, AvatarFallback } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";

interface AvatarProps {
  name: string;
  bgColor?: string;
  className?: string;
  iconClassName?: string;
  fallbackClassName?: string;
}

const Avatar = ({ name, bgColor, className, iconClassName, fallbackClassName }: AvatarProps) => {
  return (
    <UiAvatar className={className}>
      {name ? (
        <AvatarFallback
          className={cn("uppercase", fallbackClassName)}
          style={{ backgroundColor: bgColor }}
        >
          {name
            .split(" ")
            .map(word => word[0])
            .join("")
            .slice(0, 2)}
        </AvatarFallback>
      ) : (
        <UserIcon
          className={cn(
            "flex h-full w-full items-center justify-center rounded-full bg-muted stroke-1 p-2",
            iconClassName,
          )}
        />
      )}
    </UiAvatar>
  );
};

export default Avatar;

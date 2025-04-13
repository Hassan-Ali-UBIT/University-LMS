import { useTheme } from 'next-themes';
import { MoonIcon, SunIcon, CheckIcon } from 'lucide-react';
import { DropdownMenuSub, DropdownMenuSubTrigger, DropdownMenuSubContent, DropdownMenuItem } from '@/components/ui/dropdown-menu';

export const ThemeSelectorSubMenu = () => {
  const { setTheme, theme } = useTheme();

  const Wrapper: React.FC<React.PropsWithChildren> = ({ children }) => (
    <span className="flex items-center space-x-2.5">{children}</span>
  );
  return (
    <DropdownMenuSub>
      <DropdownMenuSubTrigger>
        <Wrapper>
          <span>Theme</span>
        </Wrapper>
      </DropdownMenuSubTrigger>

      <DropdownMenuSubContent>
        <DropdownMenuItem
          className="flex cursor-pointer items-center justify-between"
          onClick={() => setTheme('light')}
        >
          <Wrapper>
            <SunIcon className="h-4" />
            <span>Light</span>
          </Wrapper>
          {theme === 'light' && <CheckIcon className="h-4 text-green-500" />}
        </DropdownMenuItem>

        <DropdownMenuItem
          className="flex cursor-pointer items-center justify-between"
          onClick={() => setTheme('dark')}
        >
          <Wrapper>
            <MoonIcon className="h-4" />
            <span>Dark</span>
          </Wrapper>
          {theme === 'dark' && <CheckIcon className="h-4 text-green-500" />}
        </DropdownMenuItem>
      </DropdownMenuSubContent>
    </DropdownMenuSub>
  );
};

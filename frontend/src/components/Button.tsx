import type { ButtonHTMLAttributes, ReactNode } from 'react'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode
  variant?: 'primary' | 'secondary' | 'ghost'
}

export function Button({ children, variant = 'primary', className = '', ...props }: ButtonProps) {
  const variantClass = {
    primary: 'button-primary',
    secondary: 'button-secondary',
    ghost: 'button-ghost',
  }[variant]

  return (
    <button className={`${variantClass} ${className}`.trim()} {...props}>
      {children}
    </button>
  )
}

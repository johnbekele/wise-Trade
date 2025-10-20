#!/usr/bin/env bash

url="http://localhost:8000/api"

EMAIL="${EMAIL:-test@example.com}"
PASSWORD="${PASSWORD:-Secret123!}"
NEW_PASSWORD="${NEW_PASSWORD:-NewSecret123!}"
VERIFY_TOKEN="${VERIFY_TOKEN:-TOKEN}"
RESET_TOKEN="${RESET_TOKEN:-TOKEN}"

configure_vars() {
  echo "Current variables:"
  echo "EMAIL=$EMAIL"
  echo "PASSWORD=[hidden]"
  echo "NEW_PASSWORD=[hidden]"
  echo "VERIFY_TOKEN=$VERIFY_TOKEN"
  echo "RESET_TOKEN=$RESET_TOKEN"
  printf "Enter email [%s]: " "$EMAIL"; read -r inp; [[ -n "$inp" ]] && EMAIL="$inp"
  printf "Enter password [hidden to keep]: "; read -rs inp; echo; [[ -n "$inp" ]] && PASSWORD="$inp"
  printf "Enter new password [hidden to keep]: "; read -rs inp; echo; [[ -n "$inp" ]] && NEW_PASSWORD="$inp"
  printf "Enter verify token [%s]: " "$VERIFY_TOKEN"; read -r inp; [[ -n "$inp" ]] && VERIFY_TOKEN="$inp"
  printf "Enter reset token [%s]: " "$RESET_TOKEN"; read -r inp; [[ -n "$inp" ]] && RESET_TOKEN="$inp"
}

auth_test() {
  local base_url="$1"
  while true; do
    echo ""
    echo "Auth routes (@ $base_url)"
    echo "v) Configure variables"
    echo "1) Signup"
    echo "2) Login"
    echo "3) Logout"
    echo "4) Forgot Password"
    echo "5) Reset Password"
    echo "6) Verify Email"
    echo "7) Resend Verification Email"
    echo "8) Change Password"
    echo "0) Back"
    printf "Select an option: "
    read -r choice
    case "$choice" in
      v|V)
        configure_vars
        ;;
      1)
        echo "POST /auth/signup"
        read -p "Enter email: " EMAIL
        read -p "Enter password: " PASSWORD
        read -p "Enter username: " USERNAME
        read -p "Enter first name: " FIRST_NAME
        read -p "Enter last name: " LAST_NAME

        curl -s -o /dev/null -w "%{http_code}\n" -X POST "$base_url/users/signup" -H 'Content-Type: application/json' \
          -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}"
        ;;
      2)
        echo "POST /auth/login"
        curl -s -o /dev/null -w "%{http_code}\n" -X POST "$base_url/auth/login" -H 'Content-Type: application/json' \
          -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}"
        ;;
      3)
        echo "POST /auth/logout"
        curl -s -o /dev/null -w "%{http_code}\n" -X POST "$base_url/auth/logout"
        ;;
      4)
        echo "POST /auth/forgot-password"
        curl -s -o /dev/null -w "%{http_code}\n" -X POST "$base_url/auth/forgot-password" -H 'Content-Type: application/json' \
          -d "{\"email\":\"$EMAIL\"}"
        ;;
      5)
        echo "POST /auth/reset-password"
        curl -s -o /dev/null -w "%{http_code}\n" -X POST "$base_url/auth/reset-password" -H 'Content-Type: application/json' \
          -d "{\"token\":\"$RESET_TOKEN\",\"password\":\"$NEW_PASSWORD\"}"
        ;;
      6)
        echo "POST /auth/verify-email"
        curl -s -o /dev/null -w "%{http_code}\n" -X POST "$base_url/auth/verify-email" -H 'Content-Type: application/json' \
          -d "{\"token\":\"$VERIFY_TOKEN\"}"
        ;;
      7)
        echo "POST /auth/resend-verification"
        curl -s -o /dev/null -w "%{http_code}\n" -X POST "$base_url/auth/resend-verification" -H 'Content-Type: application/json' \
          -d "{\"email\":\"$EMAIL\"}"
        ;;
      8)
        echo "POST /auth/change-password"
        curl -s -o /dev/null -w "%{http_code}\n" -X POST "$base_url/auth/change-password" -H 'Content-Type: application/json' \
          -d "{\"old_password\":\"$PASSWORD\",\"new_password\":\"$NEW_PASSWORD\"}"
        ;;
      0)
        break
        ;;
      *)
        echo "Invalid option"
        ;;
    esac
  done
}


main() {
  local base_url="$1"
  while true; do
    echo ""
    echo "Router test menu (@ $base_url)"
    echo "1) Auth routes"
    echo "0) Exit"
    printf "Select an option: "
    read -r choice
    case "$choice" in
      1)
        auth_test "$base_url"
        ;;
      0)
        exit 0
        ;;
      *)
        echo "Invalid option"
        ;;
    esac
  done
}

main "$url"
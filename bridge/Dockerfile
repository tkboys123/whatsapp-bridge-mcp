FROM golang:1.21-alpine AS builder

WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY main.go ./

# Build the application
RUN go build -o bridge main.go

# Final stage
FROM alpine:latest

WORKDIR /app

# Install ca-certificates for HTTPS
RUN apk --no-cache add ca-certificates curl

# Copy binary from builder
COPY --from=builder /app/bridge .

# Create directory for database
RUN mkdir -p /app/store

# Expose port
EXPOSE 8080

# Run the bridge
CMD ["./bridge"]
